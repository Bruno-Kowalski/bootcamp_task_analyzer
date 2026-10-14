# Relatório técnico — BootCamp III | Fase 2

## Identificação

- Projeto: `bootcamp_task_analyzer`
- Repositório: <https://github.com/Bruno-Kowalski/bootcamp_task_analyzer>
- Branch de trabalho: `feature/fase1-task-analyzer`
- Data da auditoria local: 14/10/2026
- Branch publicada: `feature/fase1-task-analyzer`
- Pull Request: <https://github.com/Bruno-Kowalski/bootcamp_task_analyzer/pull/new/feature/fase1-task-analyzer>
- Vídeo: pendente, conforme escopo solicitado

## 1. Objetivo e fonte de verdade

O TaskAnalyzer foi implementado segundo a especificação SDD v1.0 em
`specs/task_analyzer_spec.md`. O PDF genérico foi tratado apenas como checklist
de entregáveis. Em caso de divergência, prevalece a especificação específica da
Fase 1.

## 2. Implementação

O módulo `src/task_analyzer.py` fornece:

- `Task`, `AnalysisResult` e `PriorityIndicator` como dataclasses;
- `Prioridade` e `Status` como enums;
- `analyze_tasks(tasks: list[Task]) -> AnalysisResult`;
- `InvalidTaskDataError` com a mensagem `Datas inválidas ou inconsistentes`;
- `NoCompletedTasksError` com a mensagem definida no contrato;
- cálculo de médias em minutos, atraso e agrupamento por prioridade;
- validação de UTC e identificadores duplicados;
- logging por meio da biblioteca padrão.

## 3. Testes e homologação

Comando executado:

```text
python -m pytest -v
```

Resultado real:

```text
15 passed in 0.03s
```

Também foi executado `python -m compileall -q src tests`, com resultado
`compileall: OK`.

O harness cobre os Cenários 1, 2 e 3, RN04, RN05, RN06, RN07, RN08,
duplicidade, lista vazia, tarefas pendentes/canceladas, prioridade sem
concluídas e prioridades compartilhadas.

## 4. Rastreabilidade

| Exigência | Especificação v1.0 | Teste/evidência |
|---|---|---|
| Cenário 1 | Seção 13.1; RN01–RN03 e RN07 | `test_acceptance_scenario_one_matches_specification` |
| Cenário 2 | Seção 13.2; RN04 | `test_scenario_two_raises_for_each_rn04_case` |
| Cenário 3 | Seção 13.3; RN05 | `test_no_completed_tasks_error_for_empty_input` |
| Casos de borda | Seções 9.3 e 10.3; RN06 e RN08 | testes de UTC, duplicidade e prioridades |
| Cálculos | Seções 7–10; RN02, RN03 e RN07 | cenário 1 e teste de arredondamento |
| Tipagem | Seções 3–5 e 16 | implementação e diagnóstico sem erros |

## 5. Uso de IA e regras de contexto

`CONTEXT_RULES.md` restringe a IA à especificação, proíbe requisitos
inventados, exige type hints, tratamento específico de exceções, testes,
logging, SRP e homologação humana. A decisão do proprietário sobre a
especificação v1.0 foi aplicada como fonte de verdade, inclusive para não
criar `TaskValidationError`, não adicionar a regra
`data_conclusao < data_criacao` e manter `NoCompletedTasksError`.

## 6. Versionamento

Foram usados commits atômicos na branch funcional. A branch funcional foi
publicada no GitHub. O Pull Request está preparado no link acima, mas a
criação exige autenticação interativa no GitHub e não foi possível concluí-la
automaticamente neste ambiente.

## 7. Evidências

As evidências textuais verificadas nesta auditoria são:

- execução verbosa do pytest: 15 testes aprovados;
- compilação Python: `compileall: OK`;
- árvore local contendo README, CONTEXT_RULES, `specs/`, `src/` e `tests/`;
- estado limpo após os commits locais.

As evidências da branch publicada podem ser verificadas no GitHub pelo link
acima. A captura do Pull Request depende da criação autenticada. O vídeo do
YouTube não faz parte deste escopo.

## 8. Conclusão

A implementação local está funcional e aderente ao contrato SDD v1.0, com a
suíte automatizada aprovada. Para concluir a entrega acadêmica, ainda é
necessário publicar a branch, abrir o Pull Request e inserir no relatório as
capturas finais do GitHub e do PR. O vídeo permanece pendente por decisão de
escopo.
