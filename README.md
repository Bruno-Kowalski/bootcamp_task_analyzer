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
    └── test_harness.py
```

---

## Responsabilidade dos Arquivos

| Arquivo / Diretório | Responsabilidade |
|---|---|
| `README.md` | Apresentação geral do projeto e orientação sobre o repositório. |
| `CONTEXT_RULES.md` | Regras persistentes de governança e desenvolvimento assistido por IA. |
| `specs/task_analyzer_spec.md` | Especificação SDD e fonte de verdade do comportamento funcional do sistema. |
| `src/task_analyzer.py` | Arquivo destinado à implementação principal do TaskAnalyzer. |
| `tests/test_harness.py` | Test harness automatizado derivado do contrato SDD. |

---

## Como executar o projeto

Os comandos abaixo devem ser executados a partir da raiz do repositório.

### 1. Pré-requisitos

- Python 3.11 ou superior;
- `pip`;
- PowerShell ou outro terminal compatível.

Para verificar a versão do Python:

```powershell
python --version
```

### 2. Criar e ativar o ambiente virtual

No Windows/PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação por política de execução, execute os
comandos usando diretamente o interpretador do ambiente virtual:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -v
```

### 3. Instalar as dependências

Com o ambiente virtual ativado:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Executar os testes

Para executar o test harness completo:

```powershell
python -m pytest -v
```

O resultado esperado é:

```text
15 passed
```

Os testes estão em [tests/test_harness.py](./tests/test_harness.py) e cobrem os
cenários de aceite, as regras de negócio e os casos de borda definidos na
especificação.

### 5. Usar o analisador em Python

O projeto é um módulo de análise em memória. Não há servidor ou banco de dados
para iniciar. Um exemplo mínimo de uso é:

```python
from datetime import datetime, timezone

from src.task_analyzer import Prioridade, Status, Task, analyze_tasks

utc = timezone.utc
dia = datetime(2026, 9, 1, tzinfo=utc)

tarefa = Task(
    id_tarefa=1,
    data_criacao=dia.replace(hour=7),
    data_inicio=dia.replace(hour=8),
    data_conclusao=dia.replace(hour=10),
    prazo=dia.replace(hour=11),
    prioridade=Prioridade.ALTA,
    status=Status.CONCLUIDA,
)

resultado = analyze_tasks([tarefa])
print(resultado.tempo_medio_conclusao_min)
print(resultado.taxa_atraso_percentual)
```

Para executar esse exemplo, salve-o temporariamente em um arquivo na raiz do
projeto, como `example.py`, e rode:

```powershell
python .\example.py
```

O arquivo de exemplo não faz parte do projeto e não deve ser criado com
credenciais ou dados sensíveis.

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
- datas inválidas ou inconsistentes lançam `InvalidTaskDataError` com a mensagem
  `Datas inválidas ou inconsistentes`;
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

## Variáveis de ambiente

Informações sensíveis e configurações específicas do ambiente devem ser
armazenadas no arquivo local `.env`. Esse arquivo é ignorado pelo Git e não
deve ser enviado ao GitHub. O projeto atualmente não exige variáveis de
ambiente; o arquivo existe para uso local futuro.

Nunca inclua no código ou em arquivos versionados:

- senhas;
- tokens e chaves de API;
- credenciais;
- strings de conexão;
- identificadores ou configurações privadas de serviços.

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

**Etapa atual:** implementação da Fase 1 v1.0 e validação automatizada do contrato SDD.

**Status do build:** `pytest` aprovado após a implementação da Fase 1.

---

## Tabela de rastreabilidade do enunciado

O enunciado/PDF é genérico e foi usado apenas como checklist de entregáveis.
Em qualquer divergência, prevaleceu o contrato específico da especificação
Fase 1 v1.0.

| Exigência do PDF | Item equivalente na especificação v1.0 | Teste correspondente |
|---|---|---|
| Cenário 1 | Seção 13.1; RN01–RN03 e RN07 | `test_acceptance_scenario_one_matches_specification` |
| Cenário 2 | Seção 13.2; RN04 | `test_scenario_two_raises_for_each_rn04_case` |
| Cenário 3 | Seção 13.3; RN05 | `test_no_completed_tasks_error_for_empty_input` |
| Casos de borda | Seções 9.3 e 10.3; RN06 e RN08 | testes parametrizados e testes de duplicidade/prioridade |
| Cálculos | Seções 7–10; RN02, RN03 e RN07 | cenário 1 e `test_delay_rate_is_rounded_to_two_decimal_places` |
| Tipagem e estruturas | Seções 3–5 e 15–16 | `test_acceptance_scenario_one_matches_specification` |

---

## Entregáveis da Fase 2

- [Relatório técnico em Markdown](./docs/phase2_report.md)
- [Relatório técnico em PDF](./docs/relatorio_tecnico_fase2.pdf)
- [Evidência da execução do pytest](./docs/evidence_pytest.png)
- [Evidência da árvore local](./docs/evidence_tree.png)
- [Evidência do Pull Request #1](./docs/evidence_pull_request.png)

Pull Request aberto:

<https://github.com/Bruno-Kowalski/bootcamp_task_analyzer/pull/1>

O vídeo de apresentação não está incluído neste escopo.

---

## Autor

**Bruno dos Santos**  
Curso: **Análise e Desenvolvimento de Sistemas**  
Disciplina: **BootCamp III**
