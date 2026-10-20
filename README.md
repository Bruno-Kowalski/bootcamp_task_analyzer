# TaskAnalyzer

[![CI](https://github.com/Bruno-Kowalski/bootcamp_task_analyzer/actions/workflows/ci.yml/badge.svg)](https://github.com/Bruno-Kowalski/bootcamp_task_analyzer/actions/workflows/ci.yml)

Projeto acadêmico desenvolvido para a disciplina **BootCamp III**, com foco em **Specification-Driven Development (SDD)** e desenvolvimento assistido por Inteligência Artificial.

O **TaskAnalyzer** tem como objetivo analisar um conjunto de tarefas e gerar indicadores de produtividade a partir de regras previamente definidas em uma especificação funcional.

> Nesta etapa, o foco do projeto está na definição do contrato SDD, das regras de contexto para agentes de IA e da estrutura que será utilizada durante a implementação.

---

## Objetivo

O módulo deverá analisar tarefas recebidas em memória e gerar os seguintes indicadores:

- tempo médio de conclusão em horas;
- totais de tarefas, concluídas e pendentes;
- taxa de atraso;
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
├── .github/
│   └── workflows/
│       └── ci.yml
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── README.md
├── CONTEXT_RULES.md
├── specs/
│   ├── requirements.yaml
│   ├── system_design_document.pdf
│   └── task_analyzer_spec.md
├── docs/
│   └── artefatos e relatório técnico da Fase 2
├── requirements.txt
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
| `specs/requirements.yaml` | Representação estruturada da especificação v1.0 e sua rastreabilidade. |
| `specs/system_design_document.pdf` | Documento de projeto exportado da especificação, fornecido separadamente. |
| `docs/` | Relatório técnico e evidências da Fase 2. |
| `.github/workflows/ci.yml` | Workflow de integração contínua para execução dos testes. |
| `Dockerfile` | Imagem isolada para execução do test harness. |
| `docker-compose.yml` | Serviço para execução dos testes em container. |
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
python -m pytest tests/test_harness.py -v
```

O resultado esperado é:

```text
5 passed
```

### 5. Executar com Docker

Para construir a imagem:

```powershell
docker build -t bootcamp-task-analyzer:local .
```

Para executar os testes diretamente na imagem:

```powershell
docker run --rm bootcamp-task-analyzer:local
```

Para executar o serviço de testes pelo Docker Compose:

```powershell
docker compose run --rm tests
```

O arquivo `.dockerignore` impede que o `.env`, caches, o ambiente virtual,
documentação e metadados do Git sejam incluídos na imagem.

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
print(resultado.total_tarefas)
print(resultado.total_concluidas)
print(resultado.total_pendentes)
print(resultado.tempo_medio_conclusao_horas)
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

### Indicadores retornados

O objeto `AnalysisResult` contém:

- `total_tarefas`: quantidade de tarefas válidas;
- `total_concluidas`: quantidade de tarefas concluídas;
- `total_pendentes`: quantidade de tarefas pendentes;
- `tempo_medio_conclusao_horas`: média do tempo de conclusão em horas;
- `taxa_atraso_percentual`: percentual de tarefas concluídas após o prazo;
- `indicadores_por_prioridade`: indicadores agrupados por prioridade.

Cada indicador de prioridade contém os mesmos totais e médias referentes
exclusivamente àquela prioridade. Quando não existem tarefas concluídas, as
médias e a taxa de atraso retornam `0.0`.

Entre as principais regras previstas estão:

- somente tarefas válidas participam dos resultados;
- somente tarefas concluídas válidas participam dos cálculos de tempo e atraso;
- datas e horários devem respeitar as regras de UTC;
- identificadores de tarefa devem ser únicos;
- tarefas pendentes ou canceladas não são consideradas atrasadas;
- datas inválidas ou inconsistentes lançam `TaskValidationError` com a mensagem
  `Datas inválidas ou inconsistentes`;
- entradas vazias ou sem tarefas concluídas retornam médias iguais a `0.0`;
- a taxa de atraso e o tempo médio em horas devem seguir exatamente as fórmulas especificadas;
- os resultados devem respeitar as estruturas `AnalysisResult` e `PriorityIndicator`;

---

## Cenários do Test Harness

O arquivo [tests/test_harness.py](./tests/test_harness.py) utiliza `pytest` e
traduz diretamente os cenários de aceite:

1. **Sucesso:** valida totais, médias em horas, taxa de atraso e indicadores
   gerais e por prioridade;
2. **Erro:** confirma que datas inconsistentes, como
   `data_conclusao < data_criacao`, lançam `TaskValidationError`;
3. **Casos de borda:** confirma que entradas vazias ou somente com tarefas
   pendentes retornam médias e taxa de atraso iguais a `0.0`, sem exceções não
   tratadas.

Para executar a suíte:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Resultado atual:

```text
5 passed
```

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

Os testes automatizados são executados com `pytest` e são derivados
diretamente da especificação SDD.

Entre os comportamentos que deverão ser validados estão:

- processamento de entradas válidas;
- cálculo do tempo de conclusão;
- cálculo do tempo médio de conclusão em horas;
- identificação de tarefas atrasadas;
- cálculo da taxa de atraso;
- totais de tarefas, concluídas e pendentes;
- agrupamento por prioridade;
- tratamento de tarefas inválidas ou inconsistentes;
- tratamento de identificadores duplicados;
- tratamento de entradas vazias ou sem tarefas concluídas, com médias iguais a
  `0.0`;
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

**Etapa atual:** Fase 3 — automação de CI/CD, containerização e preparação para homologação final.

**Status do build:** testes locais aprovados; a execução no GitHub Actions depende do push da branch e a validação Docker depende do daemon Docker disponível.

---

## Autor

**Bruno dos Santos**  
Curso: **Análise e Desenvolvimento de Sistemas**  
Disciplina: **BootCamp III**
