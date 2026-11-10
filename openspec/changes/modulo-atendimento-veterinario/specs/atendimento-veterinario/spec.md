## ADDED Requirements

### Requirement: Agenda Clínica

O sistema SHALL apresentar uma agenda para organizar os agendamentos veterinários por data e horário.

#### Scenario: Visualizar agenda

- **WHEN** o administrador acessar a tela de Atendimento Veterinário
- **THEN** o sistema SHALL apresentar os agendamentos em uma grade de horários
- **AND** SHALL permitir a navegação entre dias e semanas

#### Scenario: Identificar agendamentos

- **WHEN** os agendamentos forem exibidos
- **THEN** o sistema SHALL identificar visualmente o tipo de procedimento
- **AND** SHALL apresentar separadamente o status do atendimento

### Requirement: Cadastro de Agendamentos e Atendimentos

O sistema SHALL permitir cadastrar agendamentos e registrar os atendimentos veterinários dos animais.

#### Scenario: Cadastrar agendamento

- **WHEN** o administrador cadastrar um agendamento
- **THEN** o sistema SHALL permitir informar o animal, a data, o horário e o veterinário responsável
- **AND** SHALL registrar o status como `Agendado`

#### Scenario: Registrar atendimento realizado

- **WHEN** um atendimento for realizado
- **THEN** o sistema SHALL permitir registrar o diagnóstico, os procedimentos, o tratamento, o custo e o peso
- **AND** SHALL permitir atualizar o status para `Realizado`

#### Scenario: Cancelar agendamento

- **WHEN** um agendamento for cancelado
- **THEN** o sistema SHALL permitir atualizar seu status para `Cancelado`

### Requirement: Consulta do Histórico Veterinário

O sistema SHALL permitir consultar os registros veterinários relacionados a cada animal.

#### Scenario: Visualizar atendimentos recentes

- **WHEN** o administrador selecionar um animal
- **THEN** o sistema SHALL apresentar os três atendimentos realizados mais recentes, quando disponíveis

#### Scenario: Consultar histórico completo

- **WHEN** o administrador solicitar o histórico completo
- **THEN** o sistema SHALL apresentar os registros veterinários do animal selecionado

#### Scenario: Preservar registros anteriores

- **WHEN** o administrador consultar um atendimento já realizado
- **THEN** o sistema SHALL permitir visualizar suas informações sem alterá-las

### Requirement: Ficha Clínica do Animal

O sistema SHALL apresentar as informações disponíveis do animal selecionado para auxiliar a consulta veterinária.

#### Scenario: Visualizar informações clínicas

- **WHEN** o administrador selecionar um animal
- **THEN** o sistema SHALL apresentar seus dados disponíveis, incluindo nome, espécie, raça, idade estimada, sexo e condição de saúde

#### Scenario: Visualizar alertas clínicos

- **WHEN** o animal possuir alergias ou restrições clínicas cadastradas
- **THEN** o sistema SHALL destacar essas informações na ficha clínica

#### Scenario: Consultar peso

- **WHEN** existirem registros de atendimentos realizados
- **THEN** o sistema SHALL permitir consultar o peso registrado nos atendimentos