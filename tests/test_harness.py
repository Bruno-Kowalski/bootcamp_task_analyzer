"""Acceptance and edge-case tests for the Phase 1 v1.0 contract."""

from datetime import datetime, timedelta, timezone

import pytest

from src.task_analyzer import (
    AnalysisResult,
    InvalidTaskDataError,
    NoCompletedTasksError,
    Prioridade,
    PriorityIndicator,
    Status,
    Task,
    analyze_tasks,
)


UTC = timezone.utc


def task(
    task_id: int,
    *,
    status: Status = Status.CONCLUIDA,
    priority: Prioridade = Prioridade.ALTA,
    start_hour: int | None = 8,
    completion_hour: int | None = 11,
    deadline_hour: int = 10,
    created_hour: int = 7,
) -> Task:
    """Build a task with UTC dates for the harness."""
    date = datetime(2026, 9, 1, tzinfo=UTC)
    return Task(
        id_tarefa=task_id,
        data_criacao=date.replace(hour=created_hour),
        data_inicio=(
            date.replace(hour=start_hour) if start_hour is not None else None
        ),
        data_conclusao=(
            date.replace(hour=completion_hour)
            if completion_hour is not None
            else None
        ),
        prazo=date.replace(hour=deadline_hour),
        prioridade=priority,
        status=status,
    )


def test_acceptance_scenario_one_matches_specification() -> None:
    # Especificação 13.1 / RN01-RN03, RN07, seção 20: cenário 1.
    result = analyze_tasks(
        [
            task(1, priority=Prioridade.ALTA),
            task(
                2,
                priority=Prioridade.BAIXA,
                start_hour=9,
                completion_hour=10,
                deadline_hour=11,
                created_hour=8,
            ),
            task(
                3,
                status=Status.PENDENTE,
                priority=Prioridade.ALTA,
                start_hour=None,
                completion_hour=None,
                deadline_hour=18,
                created_hour=9,
            ),
        ]
    )

    assert isinstance(result, AnalysisResult)
    assert result.quantidade_tarefas == 3
    assert result.taxa_atraso_percentual == pytest.approx(50.0)
    assert result.tempo_medio_conclusao_min == pytest.approx(120.0)
    assert result.indicadores_por_prioridade["alta"] == PriorityIndicator(
        quantidade=2, quantidade_atrasadas=1, tempo_medio_conclusao=180.0
    )
    assert result.indicadores_por_prioridade["baixa"] == PriorityIndicator(
        quantidade=1, quantidade_atrasadas=0, tempo_medio_conclusao=60.0
    )
    assert "media" not in result.indicadores_por_prioridade


@pytest.mark.parametrize(
    "invalid_task",
    [
        # Especificação 12.1 / RN04: concluída sem data_inicio.
        task(1, start_hour=None),
        # Especificação 12.1 / RN04: concluída sem data_conclusao.
        task(1, completion_hour=None),
        # Especificação 12.1 / RN04: conclusão anterior ao início.
        task(1, start_hour=12, completion_hour=11),
        # Especificação 12.1 / RN04: data sem fuso UTC.
        task(1),
    ],
)
def test_scenario_two_raises_for_each_rn04_case(
    invalid_task: Task,
) -> None:
    # Especificação 13.2 / RN04 e seção 20: dados de data inválidos.
    if invalid_task.data_inicio is not None and invalid_task.data_conclusao is not None:
        if invalid_task.data_inicio.hour == 8 and invalid_task.data_conclusao.hour == 11:
            invalid_task = Task(
                **{
                    **invalid_task.__dict__,
                    "data_criacao": invalid_task.data_criacao.replace(tzinfo=None),
                }
            )
    with pytest.raises(
        InvalidTaskDataError, match="^Datas inválidas ou inconsistentes$"
    ):
        analyze_tasks([invalid_task])


def test_no_completed_tasks_error_for_empty_input() -> None:
    # Especificação 13.3 / RN05 e seção 20: entrada sem concluídas válidas.
    with pytest.raises(
        NoCompletedTasksError,
        match="^Não existem tarefas concluídas válidas para realizar a análise\\.$",
    ):
        analyze_tasks([])


@pytest.mark.parametrize(
    "tasks",
    [
        [task(1, status=Status.PENDENTE, start_hour=None, completion_hour=None)],
        [task(1, status=Status.CANCELADA, start_hour=None, completion_hour=None)],
    ],
)
def test_only_pending_or_cancelled_tasks_raise_no_completed_error(
    tasks: list[Task],
) -> None:
    # Especificação 9.3 / RN05 e seção 20: pendentes/canceladas sem concluídas.
    with pytest.raises(NoCompletedTasksError):
        analyze_tasks(tasks)


def test_duplicate_ids_are_all_invalid() -> None:
    # Especificação RN08 e seção 20: identificador duplicado.
    with pytest.raises(NoCompletedTasksError):
        analyze_tasks([task(1), task(1, priority=Prioridade.BAIXA)])


@pytest.mark.parametrize("offset", [None, timedelta(hours=1)])
def test_non_utc_datetime_is_invalid(offset: timedelta | None) -> None:
    # Especificação RN04/RN06 e seção 20: datetime sem UTC ou em outro fuso.
    value = datetime(2026, 9, 1, 8, tzinfo=UTC if offset is None else timezone(offset))
    if offset is None:
        value = value.replace(tzinfo=None)
    invalid = task(1)
    invalid = Task(**{**invalid.__dict__, "data_inicio": value})
    with pytest.raises(InvalidTaskDataError):
        analyze_tasks([invalid])


def test_priority_with_only_pending_tasks_has_zero_average() -> None:
    # Especificação 9.3 / 10.3 e seção 20: prioridade sem concluídas.
    result = analyze_tasks(
        [
            task(1, priority=Prioridade.ALTA),
            task(
                2,
                status=Status.PENDENTE,
                priority=Prioridade.MEDIA,
                start_hour=None,
                completion_hour=None,
            ),
        ]
    )
    assert result.indicadores_por_prioridade["media"].tempo_medio_conclusao == 0.0


def test_delay_rate_is_rounded_to_two_decimal_places() -> None:
    # Especificação RN07 e seção 20: arredondamento da taxa em duas casas.
    tasks = [
        task(1, deadline_hour=10),
        task(2, deadline_hour=11),
        task(3, deadline_hour=11),
    ]
    result = analyze_tasks(tasks)
    assert result.taxa_atraso_percentual == pytest.approx(33.33)


def test_priority_without_valid_tasks_is_absent() -> None:
    # Especificação 10 / RN04 e seção 20: prioridade inválida ausente.
    valid = task(1, priority=Prioridade.ALTA)
    invalid = Task(**{**task(2, priority=Prioridade.MEDIA).__dict__, "data_inicio": datetime(2026, 9, 1, 8)})
    with pytest.raises(InvalidTaskDataError):
        analyze_tasks([valid, invalid])


def test_completed_tasks_can_share_one_priority() -> None:
    # Especificação 10 e seção 20: indicadores apenas da prioridade presente.
    result = analyze_tasks(
        [task(1, priority=Prioridade.BAIXA), task(2, priority=Prioridade.BAIXA)]
    )
    assert set(result.indicadores_por_prioridade) == {"baixa"}