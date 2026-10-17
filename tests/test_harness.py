"""Test Harness pytest para os cenários de aceite do TaskAnalyzer."""

from datetime import datetime, timezone

import pytest

from src.task_analyzer import (
    AnalysisResult,
    PriorityIndicator,
    Prioridade,
    Status,
    Task,
    TaskValidationError,
    analyze_tasks,
)


UTC = timezone.utc


def criar_tarefa(
    id_tarefa: int,
    *,
    status: Status = Status.CONCLUIDA,
    prioridade: Prioridade = Prioridade.ALTA,
    hora_criacao: int = 7,
    hora_inicio: int | None = 8,
    hora_conclusao: int | None = 11,
    hora_prazo: int = 10,
) -> Task:
    """Cria uma tarefa com datas UTC para os cenários de teste."""
    data = datetime(2026, 9, 1, tzinfo=UTC)
    return Task(
        id_tarefa=id_tarefa,
        data_criacao=data.replace(hour=hora_criacao),
        data_inicio=(
            data.replace(hour=hora_inicio) if hora_inicio is not None else None
        ),
        data_conclusao=(
            data.replace(hour=hora_conclusao)
            if hora_conclusao is not None
            else None
        ),
        prazo=data.replace(hour=hora_prazo),
        prioridade=prioridade,
        status=status,
    )


def test_analise_calcula_totais_medias_e_atrasos() -> None:
    """Cenário 1: calcula os indicadores gerais e por prioridade."""
    resultado = analyze_tasks(
        [
            criar_tarefa(1, prioridade=Prioridade.ALTA),
            criar_tarefa(
                2,
                prioridade=Prioridade.BAIXA,
                hora_inicio=9,
                hora_conclusao=10,
                hora_prazo=11,
                hora_criacao=8,
            ),
            criar_tarefa(
                3,
                status=Status.PENDENTE,
                prioridade=Prioridade.ALTA,
                hora_inicio=None,
                hora_conclusao=None,
                hora_prazo=18,
                hora_criacao=9,
            ),
        ]
    )

    assert isinstance(resultado, AnalysisResult)
    assert resultado.total_tarefas == 3
    assert resultado.total_concluidas == 2
    assert resultado.total_pendentes == 1
    assert resultado.tempo_medio_conclusao_horas == pytest.approx(2.0)
    assert resultado.taxa_atraso_percentual == pytest.approx(50.0)
    assert resultado.indicadores_por_prioridade["alta"] == PriorityIndicator(
        total_tarefas=2,
        total_concluidas=1,
        total_pendentes=1,
        tempo_medio_conclusao_horas=3.0,
        taxa_atraso_percentual=100.0,
    )
    assert resultado.indicadores_por_prioridade["baixa"] == PriorityIndicator(
        total_tarefas=1,
        total_concluidas=1,
        total_pendentes=0,
        tempo_medio_conclusao_horas=1.0,
        taxa_atraso_percentual=0.0,
    )


def test_data_inconsistente_gera_erro() -> None:
    """Cenário 2: conclusão anterior à criação dispara validação."""
    tarefa = criar_tarefa(1, hora_criacao=12, hora_conclusao=11)

    with pytest.raises(TaskValidationError):
        analyze_tasks([tarefa])


@pytest.mark.parametrize(
    "tarefas",
    [
        pytest.param([], id="entrada_vazia"),
        pytest.param(
            [
                criar_tarefa(
                    1,
                    status=Status.PENDENTE,
                    hora_inicio=None,
                    hora_conclusao=None,
                )
            ],
            id="somente_tarefas_pendentes",
        ),
    ],
)
def test_entrada_sem_concluidas_retorna_zeros(tarefas: list[Task]) -> None:
    """Casos de borda: entradas sem concluídas retornam indicadores zero."""
    resultado = analyze_tasks(tarefas)

    assert resultado.total_concluidas == 0
    assert resultado.tempo_medio_conclusao_horas == 0.0
    assert resultado.taxa_atraso_percentual == 0.0


def test_media_da_prioridade_sem_concluidas_e_zero() -> None:
    """Caso de borda: média da prioridade pendente permanece em zero."""
    resultado = analyze_tasks(
        [
            criar_tarefa(1, prioridade=Prioridade.ALTA),
            criar_tarefa(
                2,
                status=Status.PENDENTE,
                prioridade=Prioridade.MEDIA,
                hora_inicio=None,
                hora_conclusao=None,
            ),
        ]
    )

    assert (
        resultado.indicadores_por_prioridade["media"].tempo_medio_conclusao_horas
        == 0.0
    )
