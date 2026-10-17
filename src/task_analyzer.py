"""Análise de tarefas conforme a especificação da Fase 1 v1.0."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import logging
from typing import Iterable


REGISTRADOR = logging.getLogger(__name__)
MENSAGEM_DADOS_TAREFA_INVALIDOS = "Datas inválidas ou inconsistentes"


class TaskValidationError(ValueError):
    """Indica que uma tarefa contém dados inválidos ou inconsistentes."""


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
    """Indicadores consolidados das tarefas de uma prioridade."""

    total_tarefas: int
    total_concluidas: int
    total_pendentes: int
    tempo_medio_conclusao_horas: float
    taxa_atraso_percentual: float


@dataclass(frozen=True)
class AnalysisResult:
    """Indicadores consolidados de uma coleção de tarefas."""

    total_tarefas: int
    total_concluidas: int
    total_pendentes: int
    tempo_medio_conclusao_horas: float
    taxa_atraso_percentual: float
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
    """Valida as datas aplicáveis e sua ordem cronológica."""
    datas = (task.data_criacao, task.data_inicio, task.data_conclusao, task.prazo)
    if any(valor is not None and not _eh_datetime_utc(valor) for valor in datas):
        raise TaskValidationError(MENSAGEM_DADOS_TAREFA_INVALIDOS)

    if task.status is Status.CONCLUIDA:
        if task.data_inicio is None or task.data_conclusao is None:
            raise TaskValidationError(MENSAGEM_DADOS_TAREFA_INVALIDOS)
        if task.data_conclusao < task.data_criacao:
            raise TaskValidationError(MENSAGEM_DADOS_TAREFA_INVALIDOS)
        if task.data_conclusao < task.data_inicio:
            raise TaskValidationError(MENSAGEM_DADOS_TAREFA_INVALIDOS)


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


def _criar_indicador(
    tarefas: list[Task],
    tarefas_concluidas: list[Task],
) -> PriorityIndicator:
    """Calcula os indicadores de um conjunto de tarefas."""
    tempos = [
        _calcular_minutos_de_conclusao(tarefa) for tarefa in tarefas_concluidas
    ]
    atrasadas = [
        tarefa
        for tarefa in tarefas_concluidas
        if tarefa.data_conclusao > tarefa.prazo
    ]
    return PriorityIndicator(
        total_tarefas=len(tarefas),
        total_concluidas=len(tarefas_concluidas),
        total_pendentes=sum(tarefa.status is Status.PENDENTE for tarefa in tarefas),
        tempo_medio_conclusao_horas=(
            sum(tempos) / len(tempos) / 60 if tempos else 0.0
        ),
        taxa_atraso_percentual=(
            round(len(atrasadas) / len(tarefas_concluidas) * 100, 2)
            if tarefas_concluidas
            else 0.0
        ),
    )


def analyze_tasks(tasks: list[Task]) -> AnalysisResult:
    """Analisa tarefas e retorna os indicadores exigidos pela especificação.

    Args:
        tasks: Tarefas a serem validadas e analisadas.

    Returns:
        Indicadores consolidados das tarefas e prioridades.

    Raises:
        TaskValidationError: Se uma tarefa violar as regras de data.
    """
    lista_de_tarefas = list(tasks) if isinstance(tasks, Iterable) else []
    tarefas_validas = _tarefas_validas_sem_duplicidade(lista_de_tarefas)
    tarefas_concluidas = [
        tarefa for tarefa in tarefas_validas if tarefa.status is Status.CONCLUIDA
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
        indicadores[prioridade.value] = _criar_indicador(
            tarefas_da_prioridade,
            tarefas_concluidas_da_prioridade,
        )

    indicador_geral = _criar_indicador(tarefas_validas, tarefas_concluidas)
    return AnalysisResult(
        total_tarefas=indicador_geral.total_tarefas,
        total_concluidas=indicador_geral.total_concluidas,
        total_pendentes=indicador_geral.total_pendentes,
        tempo_medio_conclusao_horas=indicador_geral.tempo_medio_conclusao_horas,
        taxa_atraso_percentual=indicador_geral.taxa_atraso_percentual,
        indicadores_por_prioridade=indicadores,
    )