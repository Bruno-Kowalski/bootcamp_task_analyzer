# Relatório técnico — BootCamp III | Fase 2

## Identificação

- Projeto: `bootcamp_task_analyzer`
- Repositório: <https://github.com/Bruno-Kowalski/bootcamp_task_analyzer>
- Branch de trabalho: `feature/fase1-task-analyzer`
- Data da auditoria local: 14/10/2026
- Branch publicada: `feature/fase1-task-analyzer`
- Pull Request #1 (implementação): <https://github.com/Bruno-Kowalski/bootcamp_task_analyzer/pull/1>
- Pull Request #2 (instruções de execução): <https://github.com/Bruno-Kowalski/bootcamp_task_analyzer/pull/2>
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

## 5. Uso de IA, prompts e regras de contexto

Durante o desenvolvimento foram utilizados prompts orientados por requisitos,
com a especificação e as regras de contexto como fontes de restrição. Os
principais prompts foram:

1. **Implementação orientada à especificação:** solicitação para implementar o
   TaskAnalyzer em Python 3.11+, seguindo a especificação Fase 1 v1.0, com
   dataclasses, enums, type hints, logging, exceções específicas e testes
   derivados dos cenários de aceite.
2. **Correção de divergências:** instrução explícita para tratar a
   especificação v1.0 como fonte de verdade absoluta, sem criar
   `TaskValidationError`, sem adicionar campos ou regras não previstas e sem
   alterar testes para acomodar a implementação.
3. **Proteção de configuração:** solicitação para criar o `.env`, manter dados
   locais fora do GitHub e atualizar o `.gitignore`, sem inserir segredos no
   repositório.
4. **Documentação e execução:** solicitação para atualizar o README com a
   estrutura do projeto, instruções de ambiente virtual, instalação de
   dependências e execução do `pytest`.
5. **Tradução do código:** solicitação para traduzir docstrings, variáveis
   internas, funções auxiliares e logs para pt-BR, preservando os nomes de
   arquivos e a API pública exigida pelo contrato.

`CONTEXT_RULES.md` restringe a IA à especificação, proíbe requisitos
inventados, exige type hints, tratamento específico de exceções, testes,
logging, SRP e homologação humana. A decisão do proprietário sobre a
especificação v1.0 foi aplicada como fonte de verdade, inclusive para não
criar `TaskValidationError`, não adicionar a regra
`data_conclusao < data_criacao` e manter `NoCompletedTasksError`.

Na prática, essas regras evitaram "alucinações" do assistente porque:

- obrigaram a consultar a especificação antes de alterar comportamento;
- proibiram inferir regras a partir do PDF genérico quando havia divergência;
- impediram a criação de campos, exceções e validações não autorizados;
- exigiram rastreabilidade entre requisito, implementação e teste;
- determinaram que ambiguidades fossem submetidas à revisão humana;
- exigiram execução dos testes e homologação antes de considerar a entrega
  concluída.

## 6. Versionamento

Foram usados commits atômicos na branch funcional. A branch funcional foi
publicada no GitHub. O Pull Request #1 foi mesclado na `main`, e o Pull Request
#2, que atualizou as instruções de execução, também foi mesclado.

## 7. Evidências

As evidências da entrega incluem:

- **Execução e aprovação dos testes:** `docs/evidence_pytest.png` e
  `docs/evidence_pytest.txt`, demonstrando `15 passed in 0.03s`;
- **Árvore de arquivos publicada:** `docs/evidence_tree.png` e
  `docs/evidence_tree.txt`, com README, CONTEXT_RULES, `specs/`, `src/`,
  `tests/` e `docs/`;
- **Pull Request:** `docs/evidence_pull_request.png`, demonstrando o fluxo do
  Pull Request no GitHub;
- **Relato de prompts e prevenção de alucinações:** seção 5 deste relatório;
- compilação Python: `compileall: OK`.

Os PRs publicados estão disponíveis em
<https://github.com/Bruno-Kowalski/bootcamp_task_analyzer/pulls>. O vídeo do
YouTube não faz parte deste escopo.

## 8. Conclusão

A implementação está funcional e aderente ao contrato SDD v1.0, com a suíte
automatizada aprovada. O relatório contém as evidências de terminal, árvore do
repositório, Pull Requests e uso de IA exigidas para a Fase 2. O vídeo
permanece pendente por decisão de escopo.
