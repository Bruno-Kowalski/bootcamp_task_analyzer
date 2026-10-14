"""Análise de tarefas conforme a especificação da Fase 1 v1.0."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import logging
from typing import Iterable


REGISTRADOR = logging.getLogger(__name__)
MENSAGEM_DADOS_TAREFA_INVALIDOS = "Datas inválidas ou inconsistentes"
MENSAGEM_NENHUMA_TAREFA_CONCLUIDA = (
    "Não existem tarefas concluídas válidas para realizar a análise."
)


class InvalidTaskDataError(ValueError):
    """Indica que uma tarefa contém datas inválidas ou inconsistentes."""


class NoCompletedTasksError(ValueError):
    """Indica que não há tarefa concluída válida para análise."""


class Prioridade(str, Enum):
    """Prioridades de tarefa permitidas."""

    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"


class Status(str, Enum):
    """Status de tarefa permitidos."""

    CONCLUIDA = "concluida"
    PENDENTE = "pendente"
    CANCELADA = "cancelada"


@dataclass(frozen=True)
class Task:
    """Tarefa a ser analisada."""

    id_tarefa: int
    data_criacao: datetime
    data_inicio: datetime | None
    data_conclusao: datetime | None
    prazo: datetime
    prioridade: Prioridade
    status: Status


@dataclass(frozen=True)
class PriorityIndicator:
    """Indicadores consolidados de uma prioridade."""

    quantidade: int
    quantidade_atrasadas: int
    tempo_medio_conclusao: float


@dataclass(frozen=True)
class AnalysisResult:
    """Indicadores consolidados de uma coleção de tarefas."""

    tempo_medio_conclusao_min: float
    taxa_atraso_percentual: float
    quantidade_tarefas: int
    indicadores_por_prioridade: dict[str, PriorityIndicator]


def _eh_datetime_utc(value: object) -> bool:
    """Retorna se o valor é um datetime UTC com fuso horário."""
    if not isinstance(value, datetime) or value.tzinfo is None:
        return False
    try:
        return value.utcoffset() == timedelta(0)
    except (TypeError, ValueError):
        return False


def _validar_dados_de_data(task: Task) -> None:
    """Valida as datas aplicáveis e as regras de consistência da RN04."""
    datas = (task.data_criacao, task.data_inicio, task.data_conclusao, task.prazo)
    if any(valor is not None and not _eh_datetime_utc(valor) for valor in datas):
        raise InvalidTaskDataError(MENSAGEM_DADOS_TAREFA_INVALIDOS)

    if task.status is Status.CONCLUIDA:
        if task.data_inicio is None or task.data_conclusao is None:
            raise InvalidTaskDataError(MENSAGEM_DADOS_TAREFA_INVALIDOS)
        if task.data_conclusao < task.data_inicio:
            raise InvalidTaskDataError(MENSAGEM_DADOS_TAREFA_INVALIDOS)


def _tarefas_validas_sem_duplicidade(tarefas: list[Task]) -> list[Task]:
    """Retorna tarefas válidas após regras de data e de ID duplicado."""
    contagens: dict[int, int] = {}
    for tarefa in tarefas:
        if isinstance(tarefa, Task):
            contagens[tarefa.id_tarefa] = contagens.get(tarefa.id_tarefa, 0) + 1

    tarefas_validas: list[Task] = []
    for tarefa in tarefas:
        if not isinstance(tarefa, Task):
            continue
        if not isinstance(tarefa.id_tarefa, int) or tarefa.id_tarefa <= 0:
            continue
        if not isinstance(tarefa.prioridade, Prioridade) or not isinstance(
            tarefa.status, Status
        ):
            continue
        _validar_dados_de_data(tarefa)
        if contagens[tarefa.id_tarefa] != 1:
            REGISTRADOR.warning("Ignorando ID de tarefa duplicado: %s", tarefa.id_tarefa)
            continue
        tarefas_validas.append(tarefa)
    return tarefas_validas


def _calcular_minutos_de_conclusao(tarefa: Task) -> float:
    """Calcula o tempo de conclusão em minutos de uma tarefa concluída."""
    assert tarefa.data_inicio is not None
    assert tarefa.data_conclusao is not None
    return (tarefa.data_conclusao - tarefa.data_inicio).total_seconds() / 60


def analyze_tasks(tasks: list[Task]) -> AnalysisResult:
    """Analisa tarefas e retorna os indicadores exigidos pela especificação.

    Args:
        tasks: Tarefas a serem validadas e analisadas.

    Returns:
        Indicadores consolidados das tarefas e prioridades.

    Raises:
        InvalidTaskDataError: Se uma tarefa violar as regras de data da RN04.
        NoCompletedTasksError: Se não restar nenhuma tarefa concluída válida.
    """
    lista_de_tarefas = list(tasks) if isinstance(tasks, Iterable) else []
    tarefas_validas = _tarefas_validas_sem_duplicidade(lista_de_tarefas)
    tarefas_concluidas = [
        tarefa for tarefa in tarefas_validas if tarefa.status is Status.CONCLUIDA
    ]
    if not tarefas_concluidas:
        REGISTRADOR.info("Não há tarefas concluídas válidas para análise")
        raise NoCompletedTasksError(MENSAGEM_NENHUMA_TAREFA_CONCLUIDA)

    tempos_de_conclusao = {
        id(tarefa): _calcular_minutos_de_conclusao(tarefa)
        for tarefa in tarefas_concluidas
    }
    tarefas_atrasadas = [
        tarefa for tarefa in tarefas_concluidas if tarefa.data_conclusao > tarefa.prazo
    ]
    indicadores: dict[str, PriorityIndicator] = {}
    for prioridade in Prioridade:
        tarefas_da_prioridade = [
            tarefa for tarefa in tarefas_validas if tarefa.prioridade is prioridade
        ]
        if not tarefas_da_prioridade:
            continue
        tarefas_concluidas_da_prioridade = [
            tarefa
            for tarefa in tarefas_da_prioridade
            if tarefa.status is Status.CONCLUIDA
        ]
        indicadores[prioridade.value] = PriorityIndicator(
            quantidade=len(tarefas_da_prioridade),
            quantidade_atrasadas=sum(
                tarefa.data_conclusao > tarefa.prazo
                for tarefa in tarefas_concluidas_da_prioridade
            ),
            tempo_medio_conclusao=(
                sum(
                    tempos_de_conclusao[id(tarefa)]
                    for tarefa in tarefas_concluidas_da_prioridade
                )
                / len(tarefas_concluidas_da_prioridade)
                if tarefas_concluidas_da_prioridade
                else 0.0
            ),
        )

    return AnalysisResult(
        tempo_medio_conclusao_min=sum(tempos_de_conclusao.values())
        / len(tarefas_concluidas),
        taxa_atraso_percentual=round(
            len(tarefas_atrasadas) / len(tarefas_concluidas) * 100, 2
        ),
        quantidade_tarefas=len(tarefas_validas),
        indicadores_por_prioridade=indicadores,
    )