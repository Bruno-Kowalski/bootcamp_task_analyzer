CONTEXT_RULES - TaskAnalyzer

Este arquivo define as regras persistentes que deverão ser seguidas por qualquer agente de Inteligência Artificial utilizado no desenvolvimento do TaskAnalyzer.

O objetivo destas regras é garantir consistência, rastreabilidade, qualidade do código e aderência à especificação SDD durante todo o desenvolvimento.

1. FONTE DE VERDADE DO PROJETO

A fonte de verdade para o comportamento funcional do sistema está localizada em:

specs/task_analyzer_spec.md

Este arquivo (CONTEXT_RULES.md) constitui a fonte de verdade para as regras de governança, arquitetura, qualidade e utilização de Inteligência Artificial.

Toda implementação deverá respeitar simultaneamente os dois documentos.

A Inteligência Artificial não deverá:

inventar requisitos;

assumir comportamentos não especificados;

modificar regras de negócio;

criar novos campos, estados ou prioridades sem autorização;

alterar entradas, saídas ou assinaturas públicas sem autorização.

Caso exista ambiguidade, informação insuficiente ou aparente contradição entre os documentos, a IA não deverá decidir por conta própria qual regra prevalece. O desenvolvimento deverá ser interrompido naquele ponto e a decisão deverá ser submetida à revisão humana.

2. DIRETRIZES ARQUITETURAIS OBRIGATÓRIAS

Todo código desenvolvido para o TaskAnalyzer deverá seguir as seguintes regras:

utilizar Python 3.11 ou superior;

utilizar type hints em todas as funções e métodos;

seguir o princípio Single Responsibility Principle (SRP);

seguir as convenções da PEP 8;

utilizar Google Style Docstrings em módulos, classes, funções e métodos;

manter funções pequenas, coesas e com um único propósito;

utilizar nomes de variáveis, funções, classes e métodos descritivos;

utilizar tratamento específico de exceções;

utilizar mensagens de erro claras;

utilizar o módulo padrão logging para registros de eventos relevantes da aplicação;

evitar código duplicado;

evitar código desnecessário;

priorizar legibilidade, clareza e manutenibilidade.

3. REGRAS DE DOMÍNIO

Todas as estruturas, validações, cálculos, regras de negócio, exceções e restrições funcionais estão definidas em:

specs/task_analyzer_spec.md

A IA deverá consultar essa especificação antes de implementar ou alterar qualquer comportamento funcional.

Nenhuma regra de domínio poderá ser criada, reinterpretada ou modificada por iniciativa própria.

Em especial, deverão ser preservados:

os valores permitidos para prioridade e status;

as regras de validação e consideração das tarefas;

as regras temporais e de UTC;

as regras de unicidade de id_tarefa;

as fórmulas de cálculo;

as regras de arredondamento;

as estruturas Task, AnalysisResult e PriorityIndicator;

as exceções e suas respectivas condições de lançamento;

o comportamento definido para tarefas inválidas ou inconsistentes.

4. ASSINATURA PÚBLICA

A função pública principal deverá possuir a assinatura definida pela especificação:

def analyze_tasks(tasks: list[Task]) -> AnalysisResult:
    ...

A definição completa do comportamento da função está localizada em:

specs/task_analyzer_spec.md

A IA não poderá alterar, sem autorização humana explícita:

o nome analyze_tasks;

o parâmetro tasks;

o tipo esperado list[Task];

o tipo de retorno AnalysisResult.

5. TRATAMENTO DE EXCEÇÕES

As exceções deverão seguir exatamente o comportamento definido na especificação SDD.

A IA deverá:

utilizar exceções específicas quando previstas pelo contrato;

preservar as mensagens obrigatórias definidas na especificação;

impedir o retorno de resultados parciais quando a especificação determinar a interrupção da análise;

não substituir uma exceção específica por uma exceção genérica;

não criar novas exceções de domínio sem autorização;

não alterar o comportamento definido para tarefas inválidas ou inconsistentes.

6. TESTES AUTOMATIZADOS

Os testes automatizados deverão ser implementados utilizando pytest.

Os testes deverão ser derivados dos cenários de aceite e das regras definidas em:

specs/task_analyzer_spec.md

Os testes deverão verificar, no mínimo:

processamento de entradas válidas;

cálculo do tempo de conclusão;

cálculo do tempo médio de conclusão;

identificação de tarefas atrasadas;

cálculo da taxa de atraso;

quantidade de tarefas válidas;

agrupamento dos indicadores por prioridade;

tratamento de tarefas inválidas ou inconsistentes;

tratamento de identificadores duplicados;

tratamento da ausência de tarefas concluídas válidas;

estrutura de AnalysisResult;

estrutura de PriorityIndicator;

valores retornados conforme o contrato;

exceções e mensagens obrigatórias previstas na especificação.

Os testes fornecidos não deverão ser alterados, removidos ou adaptados para acomodar erros da implementação.

Novas funcionalidades somente poderão ser implementadas quando houver testes correspondentes.

7. PROIBIÇÕES EXPLÍCITAS

A Inteligência Artificial NÃO deverá:

utilizar bibliotecas externas não autorizadas;

alterar, remover ou adaptar testes fornecidos sem autorização;

modificar a estrutura de pastas do projeto sem autorização;

persistir dados em arquivos;

persistir dados em bancos de dados;

alterar assinaturas de funções públicas sem autorização;

implementar funcionalidades não previstas na especificação;

criar novas funcionalidades sem testes correspondentes;

inserir código duplicado;

inserir código desnecessário;

assumir comportamentos não especificados;

alterar regras de negócio para facilitar a implementação;

modificar os valores permitidos para prioridade ou status;

alterar estruturas de entrada ou saída sem autorização;

alterar fórmulas, regras de arredondamento ou critérios de validade definidos na especificação;

substituir decisões explícitas do contrato por interpretações próprias.

8. ESTRUTURA DO REPOSITÓRIO

A estrutura planejada do projeto é:

bootcamp_task_analyzer/
├── README.md
├── CONTEXT_RULES.md
├── specs/
│   └── task_analyzer_spec.md
├── src/
│   └── task_analyzer.py
└── tests/
    └── test_task_analyzer.py

Responsabilidades:

README.md: apresentar o projeto e orientar a navegação no repositório;

CONTEXT_RULES.md: definir regras persistentes de governança e desenvolvimento assistido por IA;

specs/task_analyzer_spec.md: definir o contrato funcional SDD do TaskAnalyzer;

src/task_analyzer.py: conter a implementação do módulo;

tests/test_task_analyzer.py: conter os testes automatizados derivados do contrato.

A estrutura não deverá ser alterada pela IA sem autorização humana explícita.

9. FLUXO DE DESENVOLVIMENTO ASSISTIDO POR IA

A implementação deverá seguir a seguinte sequência:

consultar CONTEXT_RULES.md;

consultar specs/task_analyzer_spec.md;

identificar a regra, requisito ou cenário relacionado à alteração;

verificar os testes existentes;

implementar somente o comportamento especificado;

criar ou executar os testes correspondentes;

verificar conformidade com a especificação SDD;

verificar conformidade com este CONTEXT_RULES.md;

revisar legibilidade, qualidade e tratamento de erros;

realizar homologação humana;

somente após aprovação humana, versionar a alteração no Git.

10. HOMOLOGAÇÃO HUMANA

Todo código produzido com auxílio de Inteligência Artificial deverá passar por revisão humana antes de ser considerado aprovado ou versionado.

A revisão deverá verificar:

conformidade com specs/task_analyzer_spec.md;

conformidade com CONTEXT_RULES.md;

execução completa dos testes automatizados;

aderência às regras de negócio;

qualidade e legibilidade do código;

tratamento adequado de erros;

ausência de código duplicado ou desnecessário;

ausência de comportamentos não especificados;

aderência à estrutura definida para o repositório.

Testes manuais complementares poderão ser realizados para validar casos de borda.

A Inteligência Artificial será utilizada como ferramenta de apoio ao desenvolvimento.

A responsabilidade final pela revisão, validação, aprovação e versionamento do código permanece humana.