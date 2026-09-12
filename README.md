# TaskAnalyzer

Projeto acadêmico desenvolvido para a disciplina **BootCamp III**, com foco em **Specification-Driven Development (SDD)** e desenvolvimento assistido por Inteligência Artificial.

O **TaskAnalyzer** tem como objetivo analisar um conjunto de tarefas e gerar indicadores de produtividade a partir de regras previamente definidas em uma especificação funcional.

> Nesta etapa, o foco do projeto está na definição do contrato SDD, das regras de contexto para agentes de IA e da estrutura que será utilizada durante a implementação.

---

## Objetivo

O módulo deverá analisar tarefas recebidas em memória e gerar os seguintes indicadores:

- tempo médio de conclusão;
- taxa de atraso;
- quantidade de tarefas válidas;
- indicadores agrupados por prioridade.

O sistema não deverá persistir dados em arquivos ou bancos de dados.

---

## Fonte de Verdade

O comportamento funcional do TaskAnalyzer está definido em:

[`specs/task_analyzer_spec.md`](./specs/task_analyzer_spec.md)

As regras de governança, arquitetura, qualidade e utilização de Inteligência Artificial estão definidas em:

[`CONTEXT_RULES.md`](./CONTEXT_RULES.md)

Toda implementação futura deverá respeitar simultaneamente esses dois documentos.

---

## Estrutura do Projeto

```text
bootcamp_task_analyzer/
├── README.md
├── CONTEXT_RULES.md
├── specs/
│   └── task_analyzer_spec.md
├── src/
│   └── task_analyzer.py
└── tests/
    └── test_task_analyzer.py
```

---

## Responsabilidade dos Arquivos

| Arquivo / Diretório | Responsabilidade |
|---|---|
| `README.md` | Apresentação geral do projeto e orientação sobre o repositório. |
| `CONTEXT_RULES.md` | Regras persistentes de governança e desenvolvimento assistido por IA. |
| `specs/task_analyzer_spec.md` | Especificação SDD e fonte de verdade do comportamento funcional do sistema. |
| `src/task_analyzer.py` | Arquivo destinado à implementação principal do TaskAnalyzer. |
| `tests/test_task_analyzer.py` | Arquivo destinado aos testes automatizados derivados do contrato SDD. |

---

## Contrato Funcional

A função pública principal planejada para o módulo é:

```python
def analyze_tasks(tasks: list[Task]) -> AnalysisResult:
    ...
```

A implementação deverá seguir integralmente o contrato definido na especificação SDD.

Entre as principais regras previstas estão:

- somente tarefas válidas participam dos resultados;
- somente tarefas concluídas válidas participam dos cálculos de tempo e atraso;
- datas e horários devem respeitar as regras de UTC;
- identificadores de tarefa devem ser únicos;
- tarefas pendentes ou canceladas não são consideradas atrasadas;
- tarefas inválidas ou inconsistentes são desconsideradas conforme o contrato;
- a taxa de atraso e o tempo médio devem seguir exatamente as fórmulas especificadas;
- os resultados devem respeitar as estruturas `AnalysisResult` e `PriorityIndicator`;
- a ausência de tarefas concluídas válidas deve gerar `NoCompletedTasksError`.

---

## Desenvolvimento Assistido por IA

A Inteligência Artificial será utilizada como ferramenta de apoio durante o desenvolvimento.

Antes de gerar ou alterar código, o agente de IA deverá consultar:

1. [`CONTEXT_RULES.md`](./CONTEXT_RULES.md);
2. [`specs/task_analyzer_spec.md`](./specs/task_analyzer_spec.md);
3. os testes automatizados existentes.

A IA não deverá:

- inventar requisitos;
- alterar regras de negócio;
- assumir comportamentos não especificados;
- modificar a assinatura pública sem autorização;
- alterar testes para acomodar erros da implementação;
- modificar a estrutura do projeto sem autorização.

A decisão final sobre qualquer implementação permanece sob responsabilidade humana.

---

## Diretrizes Técnicas

O desenvolvimento deverá seguir as seguintes diretrizes:

- **Python 3.11+**;
- **type hints** em funções e métodos;
- **PEP 8**;
- **Single Responsibility Principle (SRP)**;
- **Google Style Docstrings**;
- funções pequenas e coesas;
- tratamento específico de exceções;
- uso do módulo padrão `logging`;
- testes automatizados com `pytest`;
- código legível, manutenível e sem duplicação desnecessária.

---

## Testes

Os testes automatizados serão implementados com `pytest` e deverão ser derivados diretamente da especificação SDD.

Entre os comportamentos que deverão ser validados estão:

- processamento de entradas válidas;
- cálculo do tempo de conclusão;
- cálculo do tempo médio de conclusão;
- identificação de tarefas atrasadas;
- cálculo da taxa de atraso;
- quantidade de tarefas válidas;
- agrupamento por prioridade;
- tratamento de tarefas inválidas ou inconsistentes;
- tratamento de identificadores duplicados;
- tratamento da ausência de tarefas concluídas válidas;
- estrutura dos objetos de saída;
- exceções e mensagens previstas no contrato.

---

## Fluxo de Desenvolvimento

```text
Especificação SDD
        ↓
Regras de contexto da IA
        ↓
Implementação
        ↓
Testes automatizados
        ↓
Revisão e homologação humana
        ↓
Versionamento no Git/GitHub
```

Todo código produzido com auxílio de Inteligência Artificial deverá passar por revisão humana antes de ser considerado aprovado.

---

## Status do Projeto

**Etapa atual:** estruturação do repositório, definição da especificação SDD e criação das regras de governança para o desenvolvimento assistido por IA.

**Próxima etapa:** implementação do TaskAnalyzer e criação dos testes automatizados com base no contrato definido.

---

## Autor

**Bruno dos Santos**  
Curso: **Análise e Desenvolvimento de Sistemas**  
Disciplina: **BootCamp III**
