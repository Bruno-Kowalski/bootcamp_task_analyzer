TaskAnalyzer

Projeto acadêmico desenvolvido para a disciplina BootCamp III, com foco em Specification-Driven Development (SDD) e desenvolvimento assistido por Inteligência Artificial.

O objetivo do projeto é especificar, implementar e validar um módulo capaz de analisar um conjunto de tarefas e gerar indicadores relacionados à produtividade.

Objetivo

O TaskAnalyzer deverá analisar tarefas recebidas em memória e gerar indicadores como:

tempo médio de conclusão;

taxa de atraso;

quantidade de tarefas válidas;

indicadores agrupados por prioridade.

O comportamento funcional do sistema é definido pela especificação SDD localizada em:

specs/task_analyzer_spec.md

Estrutura do Projeto

bootcamp_task_analyzer/
├── README.md
├── CONTEXT_RULES.md
├── specs/
│   └── task_analyzer_spec.md
├── src/
│   └── task_analyzer.py
└── tests/
    └── test_task_analyzer.py

Responsabilidade dos arquivos

README.md
Apresenta o projeto, sua finalidade e a organização do repositório.

CONTEXT_RULES.md
Define as regras persistentes de governança, arquitetura, qualidade e utilização de Inteligência Artificial durante o desenvolvimento.

specs/task_analyzer_spec.md
Contém a especificação SDD e representa a fonte de verdade para o comportamento funcional do TaskAnalyzer.

src/task_analyzer.py
Arquivo destinado à implementação do módulo TaskAnalyzer.

tests/test_task_analyzer.py
Arquivo destinado aos testes automatizados derivados dos cenários de aceite e das regras definidas na especificação.

Contrato Funcional

A função pública principal planejada para o módulo é:

def analyze_tasks(tasks: list[Task]) -> AnalysisResult:
    ...

A implementação deverá seguir integralmente o contrato definido em:

specs/task_analyzer_spec.md

Entre as principais regras previstas estão:

utilização apenas de tarefas válidas nos resultados;

utilização apenas de tarefas concluídas válidas nos cálculos de tempo e atraso;

tratamento de datas em UTC;

controle de identificadores de tarefas duplicados;

cálculo da taxa de atraso;

cálculo do tempo médio de conclusão;

geração de indicadores por prioridade;

tratamento da ausência de tarefas concluídas válidas.

Desenvolvimento Assistido por IA

A Inteligência Artificial será utilizada como ferramenta de apoio ao desenvolvimento.

Todo código gerado deverá respeitar simultaneamente:

CONTEXT_RULES.md;

specs/task_analyzer_spec.md;

os testes automatizados;

o processo de homologação humana.

A IA não deverá criar requisitos, alterar regras de negócio ou assumir comportamentos que não estejam definidos na especificação.

Diretrizes Técnicas

O desenvolvimento deverá seguir as seguintes diretrizes:

Python 3.11 ou superior;

type hints em funções e métodos;

PEP 8;

Single Responsibility Principle (SRP);

Google Style Docstrings;

funções pequenas e coesas;

tratamento específico de exceções;

uso do módulo padrão logging;

testes automatizados com pytest;

código legível e manutenível.

Testes

Os testes automatizados serão desenvolvidos com pytest e deverão validar, entre outros pontos:

processamento de entradas válidas;

cálculo do tempo de conclusão;

cálculo do tempo médio de conclusão;

identificação de tarefas atrasadas;

cálculo da taxa de atraso;

quantidade de tarefas válidas;

indicadores agrupados por prioridade;

tratamento de tarefas inválidas ou inconsistentes;

tratamento de identificadores duplicados;

tratamento da ausência de tarefas concluídas válidas;

estrutura das saídas;

exceções previstas no contrato.

Os testes deverão ser derivados diretamente da especificação SDD.

Fluxo de Desenvolvimento

O desenvolvimento seguirá, de forma geral, o seguinte fluxo:

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

Todo código produzido com auxílio de Inteligência Artificial deverá passar por revisão humana antes de ser considerado aprovado e versionado.

Status do Projeto

Fase atual: preparação da estrutura, especificação SDD e definição das regras de governança para o desenvolvimento assistido por IA.

A implementação funcional e os testes automatizados serão desenvolvidos na etapa seguinte do projeto.

Autor

Bruno dos Santos
Curso: Análise e Desenvolvimento de Sistemas
Disciplina: BootCamp III