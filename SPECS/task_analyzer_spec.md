# TaskAnalyzer - Especificação SDD

Este documento constitui a especificação funcional do módulo TaskAnalyzer e define o contrato que deverá orientar sua implementação.

Ele representa a fonte de verdade para o comportamento funcional do sistema.

O código desenvolvido deverá respeitar integralmente as entradas, saídas, regras de negócio, restrições, exceções e comportamentos definidos neste contrato.

Comportamentos não especificados não deverão ser assumidos ou implementados.

---

## 1. OBJETIVO

O TaskAnalyzer é um módulo responsável por analisar um conjunto de tarefas e gerar indicadores relacionados à produtividade.

O módulo deverá fornecer:

- tempo médio de conclusão;
- taxa de atraso;
- quantidade de tarefas válidas;
- indicadores agrupados por prioridade.

A análise deverá ser realizada exclusivamente a partir dos dados fornecidos como entrada.

Não haverá persistência de dados em arquivos ou bancos de dados.

---

## 2. INTERFACE PÚBLICA

A função pública principal deverá possuir a seguinte assinatura:

```python
def analyze_tasks(tasks: list[Task]) -> AnalysisResult:
    ...
```

A função deverá:

- receber uma coleção de tarefas por meio do parâmetro `tasks`;
- retornar um objeto `AnalysisResult` quando existir pelo menos uma tarefa concluída válida;
- lançar `NoCompletedTasksError` quando não existir nenhuma tarefa concluída válida.

A assinatura pública não deverá ser alterada sem autorização explícita.

---

## 3. ESTRUTURAS DE ENTRADA

### 3.1 Task

Cada tarefa deverá ser representada por uma estrutura `Task` contendo obrigatoriamente os seguintes campos:

```text
Task
├── id_tarefa: int
├── data_criacao: datetime
├── data_inicio: datetime | None
├── data_conclusao: datetime | None
├── prazo: datetime
├── prioridade: Prioridade
└── status: Status
```

### 3.2 Regras dos campos

#### `id_tarefa`

- deverá possuir tipo `int`;
- deverá ser maior que zero;
- deverá ser único dentro da coleção analisada.

#### `data_criacao`

- deverá possuir tipo `datetime`;
- deverá ser timezone-aware;
- deverá utilizar UTC.

#### `data_inicio`

- deverá possuir tipo `datetime` quando informada;
- poderá ser `None` quando `status = pendente` ou `status = cancelada`;
- será obrigatória quando `status = concluida`;
- quando informada, deverá ser timezone-aware em UTC.

#### `data_conclusao`

- deverá possuir tipo `datetime` quando informada;
- poderá ser `None` quando `status = pendente` ou `status = cancelada`;
- será obrigatória quando `status = concluida`;
- quando informada, deverá ser timezone-aware em UTC.

#### `prazo`

- deverá possuir tipo `datetime`;
- deverá ser timezone-aware;
- deverá utilizar UTC.

#### `prioridade`

Deverá utilizar exclusivamente um dos valores definidos pelo enum `Prioridade`.

#### `status`

Deverá utilizar exclusivamente um dos valores definidos pelo enum `Status`.

A coleção de entrada deverá ser representada por:

```python
tasks: list[Task]
```

---

## 4. ENUMERAÇÕES

### 4.1 Prioridade

Os únicos valores permitidos são:

```text
baixa
media
alta
```

Na implementação, o campo poderá ser representado pelo tipo enumerado `Prioridade`, mantendo exatamente os valores definidos neste contrato.

### 4.2 Status

Os únicos valores permitidos são:

```text
concluida
pendente
cancelada
```

Na implementação, o campo poderá ser representado pelo tipo enumerado `Status`, mantendo exatamente os valores definidos neste contrato.

---

## 5. ESTRUTURAS DE SAÍDA

### 5.1 AnalysisResult

O resultado da análise deverá possuir a estrutura:

```text
AnalysisResult
├── tempo_medio_conclusao_min: float
├── taxa_atraso_percentual: float
├── quantidade_tarefas: int
└── indicadores_por_prioridade: dict[str, PriorityIndicator]
```

Significado dos campos:

- `tempo_medio_conclusao_min`: média dos tempos de conclusão das tarefas concluídas válidas, em minutos;
- `taxa_atraso_percentual`: percentual de tarefas concluídas válidas que foram concluídas após o prazo;
- `quantidade_tarefas`: quantidade de tarefas válidas consideradas pelo analisador;
- `indicadores_por_prioridade`: indicadores agrupados pelas prioridades presentes nas tarefas válidas.

Quando não existir nenhuma tarefa concluída válida, o objeto `AnalysisResult` não deverá ser criado ou retornado.

### 5.2 PriorityIndicator

Cada entrada de `indicadores_por_prioridade` deverá possuir a estrutura:

```text
PriorityIndicator
├── quantidade: int
├── quantidade_atrasadas: int
└── tempo_medio_conclusao: float
```

O dicionário deverá utilizar o valor textual da prioridade como chave:

```python
dict[str, PriorityIndicator]
```

Somente prioridades presentes entre as tarefas válidas deverão aparecer no dicionário.

---

## 6. REGRAS DE NEGÓCIO E RESTRIÇÕES

### RN01 - Consideração das tarefas

Somente tarefas com `status = concluida` deverão participar dos cálculos de:

- tempo de conclusão;
- tempo médio de conclusão;
- identificação de atraso;
- taxa de atraso.

Tarefas com `status = pendente` ou `status = cancelada` poderão ser contabilizadas em `quantidade_tarefas` e nos indicadores de quantidade por prioridade, mas não deverão participar dos cálculos de tempo de conclusão ou atraso.

Tarefas inválidas ou inconsistentes deverão ser ignoradas conforme as regras definidas neste contrato.

### RN02 - Cálculo do tempo de conclusão

Para cada tarefa concluída válida, o tempo de conclusão deverá ser calculado pela diferença entre `data_conclusao` e `data_inicio`.

Fórmula:

```text
tempo_conclusao_min =
(data_conclusao - data_inicio).total_seconds() / 60
```

O resultado deverá:

- ser expresso em minutos;
- possuir tipo `float`.

Exemplo:

```text
data_inicio = 01/09/2026 08:00:00 UTC
data_conclusao = 01/09/2026 11:00:00 UTC

tempo_conclusao_min = 180.0
```

### RN03 - Identificação de atraso

Uma tarefa concluída válida será considerada atrasada quando:

```text
data_conclusao > prazo
```

Uma tarefa concluída exatamente no prazo não será considerada atrasada.

Tarefas pendentes ou canceladas nunca deverão ser contabilizadas como atrasadas.

### RN04 - Datas inconsistentes

Uma tarefa deverá ser considerada inconsistente quando ocorrer qualquer uma das seguintes situações:

1. `status = concluida` e `data_inicio` for `None`;
2. `status = concluida` e `data_conclusao` for `None`;
3. `data_inicio` e `data_conclusao` estiverem preenchidas e `data_conclusao < data_inicio`;
4. qualquer data obrigatória não possuir informação explícita de fuso horário UTC.

Tarefas inconsistentes deverão ser ignoradas pelo analisador e não deverão participar dos cálculos nem da contagem de `quantidade_tarefas`.

### RN05 - Ausência de tarefas concluídas válidas

Quando não existir nenhuma tarefa concluída válida no conjunto analisado, o TaskAnalyzer deverá lançar a exceção `NoCompletedTasksError`.

Nessa situação:

- nenhum objeto `AnalysisResult` deverá ser retornado;
- nenhum resultado parcial deverá ser retornado;
- a execução da análise deverá ser interrompida.

### RN06 - Fuso horário

Todo campo de data e hora com valor diferente de `None` deverá ser representado por um objeto `datetime` timezone-aware em UTC.

Objetos `datetime` sem informação de fuso horário ou associados a qualquer fuso horário diferente de UTC deverão ser considerados inválidos.

### RN07 - Arredondamento

O campo `taxa_atraso_percentual` deverá ser arredondado para duas casas decimais.

O campo `tempo_medio_conclusao_min` não deverá sofrer arredondamento obrigatório e deverá manter o resultado do cálculo como `float`.

### RN08 - Identificador de tarefa duplicado

Dentro da mesma coleção de entrada, cada `id_tarefa` deverá ser único.

Quando duas ou mais tarefas possuírem o mesmo `id_tarefa`, todas as tarefas que possuírem esse identificador duplicado deverão ser consideradas inválidas.

As tarefas com identificador duplicado não deverão participar dos cálculos nem da contagem de `quantidade_tarefas`.

---

## 7. CÁLCULO DO TEMPO MÉDIO DE CONCLUSÃO

O tempo médio de conclusão deverá ser calculado considerando somente tarefas concluídas válidas com:

- `status = concluida`;
- `data_inicio` válida;
- `data_conclusao` válida;
- datas consistentes;
- datas em UTC.

Fórmula:

```text
tempo_medio_conclusao_min =
soma dos tempos de conclusão das tarefas concluídas válidas
/
quantidade de tarefas concluídas válidas
```

O resultado deverá:

- ser expresso em minutos;
- possuir tipo `float`;
- não sofrer arredondamento obrigatório.

Quando não houver tarefas concluídas válidas, deverá ser aplicada a RN05.

---

## 8. CÁLCULO DA TAXA DE ATRASO

Somente tarefas concluídas válidas participarão do cálculo.

Fórmula:

```text
taxa_atraso_percentual =
quantidade de tarefas atrasadas
/
quantidade de tarefas concluídas válidas
* 100
```

O resultado deverá:

- possuir tipo `float`;
- ser apresentado em percentual;
- ser arredondado para duas casas decimais.

Quando não houver tarefas concluídas válidas, deverá ser aplicada a RN05.

---

## 9. QUANTIDADE DE TAREFAS

O campo `quantidade_tarefas` deverá representar a quantidade de tarefas válidas consideradas pelo analisador, independentemente do status.

Serão consideradas válidas as tarefas que:

1. possuam todos os campos obrigatórios aplicáveis ao seu status;
2. possuam `id_tarefa` maior que zero;
3. possuam prioridade pertencente ao conjunto permitido;
4. possuam status pertencente ao conjunto permitido;
5. possuam datas fornecidas em formato válido;
6. respeitem as regras de consistência de datas definidas neste contrato;
7. respeitem a regra de unicidade de `id_tarefa`.

Tarefas inválidas ou inconsistentes deverão ser ignoradas e não deverão ser contabilizadas em `quantidade_tarefas`.

---

## 10. INDICADORES POR PRIORIDADE

Os indicadores deverão ser agrupados pelas prioridades:

```text
baixa
media
alta
```

Somente prioridades que possuírem pelo menos uma tarefa válida deverão aparecer em `indicadores_por_prioridade`.

Para cada prioridade deverão ser informados:

- `quantidade`;
- `quantidade_atrasadas`;
- `tempo_medio_conclusao`.

### 10.1 Quantidade

O campo `quantidade` deverá representar o número total de tarefas válidas daquela prioridade, independentemente do status.

### 10.2 Quantidade de tarefas atrasadas

O campo `quantidade_atrasadas` deverá representar a quantidade de tarefas válidas daquela prioridade que:

1. possuam `status = concluida`;
2. possuam `data_inicio` válida;
3. possuam `data_conclusao` válida;
4. possuam datas consistentes;
5. possuam `data_conclusao > prazo`.

Tarefas pendentes ou canceladas nunca deverão ser contabilizadas como atrasadas.

### 10.3 Tempo médio de conclusão

O campo `tempo_medio_conclusao` deverá representar a média, em minutos, dos tempos de conclusão das tarefas concluídas válidas daquela prioridade.

Quando uma prioridade possuir tarefas válidas, mas nenhuma tarefa concluída válida, o valor deverá ser:

```text
tempo_medio_conclusao = 0.0
```

---

## 11. TRATAMENTO DE ERROS

### 11.1 Tarefas inválidas ou inconsistentes

Tarefas que violem as regras de validade ou consistência definidas neste contrato deverão ser ignoradas.

Elas:

- não deverão participar dos cálculos;
- não deverão participar da contagem de `quantidade_tarefas`;
- não deverão contribuir para os indicadores por prioridade.

Após o descarte dessas tarefas, as tarefas válidas restantes deverão ser processadas normalmente.

Caso, após a exclusão das tarefas inválidas ou inconsistentes, não exista nenhuma tarefa concluída válida, deverá ser aplicada a RN05.

### 11.2 NoCompletedTasksError

Quando não existir nenhuma tarefa concluída válida no conjunto analisado, o TaskAnalyzer não deverá retornar um `AnalysisResult`.

Deverá ser lançada a exceção específica:

```python
NoCompletedTasksError
```

com a mensagem obrigatória:

```text
Não existem tarefas concluídas válidas para realizar a análise.
```

O lançamento da exceção deverá interromper a execução da análise e impedir o retorno de resultados parciais.

---

## 12. CENÁRIOS DE ACEITE

### Cenário 1 - Análise realizada com sucesso

**Dado** um conjunto contendo as seguintes tarefas válidas:

#### Tarefa 1

```text
id_tarefa = 1
data_criacao = 01/09/2026 07:00:00 UTC
data_inicio = 01/09/2026 08:00:00 UTC
data_conclusao = 01/09/2026 11:00:00 UTC
prazo = 01/09/2026 10:00:00 UTC
prioridade = alta
status = concluida
```

#### Tarefa 2

```text
id_tarefa = 2
data_criacao = 01/09/2026 08:00:00 UTC
data_inicio = 01/09/2026 09:00:00 UTC
data_conclusao = 01/09/2026 10:00:00 UTC
prazo = 01/09/2026 11:00:00 UTC
prioridade = baixa
status = concluida
```

#### Tarefa 3

```text
id_tarefa = 3
data_criacao = 01/09/2026 09:00:00 UTC
data_inicio = None
data_conclusao = None
prazo = 02/09/2026 18:00:00 UTC
prioridade = alta
status = pendente
```

**Quando**:

```python
analyze_tasks(tasks)
```

for executada,

**Então** deverá ser retornado um `AnalysisResult` contendo:

```text
quantidade_tarefas = 3
tempo_medio_conclusao_min = 120.0
taxa_atraso_percentual = 50.00
```

A tarefa 1 deverá ser considerada atrasada.

A tarefa 2 não deverá ser considerada atrasada.

Os indicadores por prioridade deverão conter:

```text
alta:
    quantidade = 2
    quantidade_atrasadas = 1
    tempo_medio_conclusao = 180.0

baixa:
    quantidade = 1
    quantidade_atrasadas = 0
    tempo_medio_conclusao = 60.0
```

### Cenário 2 - Tarefas com dados inconsistentes

**Dado** um conjunto contendo pelo menos uma tarefa concluída válida e uma ou mais tarefas inconsistentes, por exemplo:

- `data_conclusao < data_inicio`;
- tarefa concluída sem `data_inicio`;
- tarefa concluída sem `data_conclusao`;
- data obrigatória sem timezone UTC.

**Quando** o TaskAnalyzer processar o conjunto,

**Então**:

- as tarefas inconsistentes deverão ser ignoradas;
- elas não deverão participar dos cálculos;
- elas não deverão participar de `quantidade_tarefas`;
- as tarefas válidas restantes deverão ser processadas normalmente.

Caso não reste nenhuma tarefa concluída válida, deverá ser aplicada a RN05.

### Cenário 3 - Ausência de tarefas concluídas válidas

**Dado** um conjunto que não possua nenhuma tarefa concluída válida,

**Quando** o TaskAnalyzer for executado,

**Então** deverá lançar:

```python
NoCompletedTasksError
```

com a mensagem:

```text
Não existem tarefas concluídas válidas para realizar a análise.
```

O sistema não deverá retornar um objeto `AnalysisResult` nem qualquer resultado parcial.

---

## 13. TEST HARNESS

Os cenários de aceite deverão servir de base para testes automatizados utilizando `pytest`.

Os testes deverão verificar, no mínimo:

- processamento de entradas válidas;
- cálculo do tempo de conclusão;
- cálculo do tempo médio de conclusão;
- identificação de tarefas atrasadas;
- cálculo da taxa de atraso;
- quantidade de tarefas válidas;
- agrupamento de indicadores por prioridade;
- tratamento de tarefas inválidas ou inconsistentes;
- tratamento de identificadores duplicados;
- tratamento da ausência de tarefas concluídas válidas;
- estrutura de `AnalysisResult`;
- estrutura de `PriorityIndicator`;
- valores retornados conforme o contrato;
- lançamento de `NoCompletedTasksError`;
- mensagem obrigatória da exceção.

Os testes fornecidos não deverão ser alterados, removidos ou adaptados para acomodar erros da implementação.

---

## 14. RESTRIÇÕES

O TaskAnalyzer não deverá:

- persistir dados em arquivos;
- persistir dados em bancos de dados;
- assumir requisitos não definidos;
- modificar regras de negócio sem autorização;
- alterar a assinatura pública sem autorização;
- retornar estruturas diferentes das definidas neste contrato;
- alterar os valores permitidos de prioridade ou status;
- alterar fórmulas ou critérios de validade sem autorização.

As regras de desenvolvimento, arquitetura, qualidade e governança para agentes de Inteligência Artificial estão definidas no arquivo:

`CONTEXT_RULES.md`
