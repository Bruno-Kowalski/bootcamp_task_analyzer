"""Task analysis according to the Phase 1 v1.0 specification."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import logging
from typing import Iterable


LOGGER = logging.getLogger(__name__)
INVALID_TASK_DATA_MESSAGE = "Datas inválidas ou inconsistentes"
NO_COMPLETED_TASKS_MESSAGE = (
    "Não existem tarefas concluídas válidas para realizar a análise."
)


class InvalidTaskDataError(ValueError):
    """Raised when a task contains invalid or inconsistent date data."""


class NoCompletedTasksError(ValueError):
    """Raised when no valid completed task is available for analysis."""


class Prioridade(str, Enum):
    """Allowed task priorities."""

    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"


class Status(str, Enum):
    """Allowed task statuses."""

    CONCLUIDA = "concluida"
    PENDENTE = "pendente"
    CANCELADA = "cancelada"


@dataclass(frozen=True)
class Task:
    """A task to be analyzed."""

    id_tarefa: int
    data_criacao: datetime
    data_inicio: datetime | None
    data_conclusao: datetime | None
    prazo: datetime
    prioridade: Prioridade
    status: Status


@dataclass(frozen=True)
class PriorityIndicator:
    """Aggregated indicators for one priority."""

    quantidade: int
    quantidade_atrasadas: int
    tempo_medio_conclusao: float


@dataclass(frozen=True)
class AnalysisResult:
    """Aggregated indicators for a collection of tasks."""

    tempo_medio_conclusao_min: float
    taxa_atraso_percentual: float
    quantidade_tarefas: int
    indicadores_por_prioridade: dict[str, PriorityIndicator]


def _is_utc_datetime(value: object) -> bool:
    """Return whether value is a timezone-aware UTC datetime."""
    if not isinstance(value, datetime) or value.tzinfo is None:
        return False
    try:
        return value.utcoffset() == timedelta(0)
    except (TypeError, ValueError):
        return False


def _validate_date_data(task: Task) -> None:
    """Validate all applicable dates and RN04 consistency rules."""
    dates = (task.data_criacao, task.data_inicio, task.data_conclusao, task.prazo)
    if any(value is not None and not _is_utc_datetime(value) for value in dates):
        raise InvalidTaskDataError(INVALID_TASK_DATA_MESSAGE)

    if task.status is Status.CONCLUIDA:
        if task.data_inicio is None or task.data_conclusao is None:
            raise InvalidTaskDataError(INVALID_TASK_DATA_MESSAGE)
        if task.data_conclusao < task.data_inicio:
            raise InvalidTaskDataError(INVALID_TASK_DATA_MESSAGE)


def _valid_unique_tasks(tasks: list[Task]) -> list[Task]:
    """Return valid tasks after applying date and duplicate-id rules."""
    counts: dict[int, int] = {}
    for task in tasks:
        if isinstance(task, Task):
            counts[task.id_tarefa] = counts.get(task.id_tarefa, 0) + 1

    valid_tasks: list[Task] = []
    for task in tasks:
        if not isinstance(task, Task):
            continue
        if not isinstance(task.id_tarefa, int) or task.id_tarefa <= 0:
            continue
        if not isinstance(task.prioridade, Prioridade) or not isinstance(
            task.status, Status
        ):
            continue
        _validate_date_data(task)
        if counts[task.id_tarefa] != 1:
            LOGGER.warning("Ignoring duplicate task id %s", task.id_tarefa)
            continue
        valid_tasks.append(task)
    return valid_tasks


def _completion_minutes(task: Task) -> float:
    """Calculate completion time in minutes for a completed task."""
    assert task.data_inicio is not None
    assert task.data_conclusao is not None
    return (task.data_conclusao - task.data_inicio).total_seconds() / 60


def analyze_tasks(tasks: list[Task]) -> AnalysisResult:
    """Analyze tasks and return the indicators required by the specification.

    Args:
        tasks: Tasks to validate and analyze.

    Returns:
        Aggregated task and priority indicators.

    Raises:
        InvalidTaskDataError: If a task violates RN04 date rules.
        NoCompletedTasksError: If no valid completed task remains.
    """
    task_list = list(tasks) if isinstance(tasks, Iterable) else []
    valid_tasks = _valid_unique_tasks(task_list)
    completed_tasks = [
        task for task in valid_tasks if task.status is Status.CONCLUIDA
    ]
    if not completed_tasks:
        LOGGER.info("No valid completed tasks available for analysis")
        raise NoCompletedTasksError(NO_COMPLETED_TASKS_MESSAGE)

    completion_times = {
        id(task): _completion_minutes(task) for task in completed_tasks
    }
    late_tasks = [
        task for task in completed_tasks if task.data_conclusao > task.prazo
    ]
    indicators: dict[str, PriorityIndicator] = {}
    for priority in Prioridade:
        priority_tasks = [
            task for task in valid_tasks if task.prioridade is priority
        ]
        if not priority_tasks:
            continue
        priority_completed = [
            task for task in priority_tasks if task.status is Status.CONCLUIDA
        ]
        indicators[priority.value] = PriorityIndicator(
            quantidade=len(priority_tasks),
            quantidade_atrasadas=sum(
                task.data_conclusao > task.prazo for task in priority_completed
            ),
            tempo_medio_conclusao=(
                sum(completion_times[id(task)] for task in priority_completed)
                / len(priority_completed)
                if priority_completed
                else 0.0
            ),
        )

    return AnalysisResult(
        tempo_medio_conclusao_min=sum(completion_times.values())
        / len(completed_tasks),
        taxa_atraso_percentual=round(
            len(late_tasks) / len(completed_tasks) * 100, 2
        ),
        quantidade_tarefas=len(valid_tasks),
        indicadores_por_prioridade=indicators,
    )