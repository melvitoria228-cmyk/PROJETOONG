# Gestão de Lares Temporários

## ADDED Requirements

### Requirement: Visualização e Consulta dos Lares Temporários

O sistema MUST apresentar os lares temporários em cards, contendo responsável, endereço, capacidade e quantidade de animais acolhidos. A tela MUST apresentar indicadores de ocupação e permitir filtrar os lares por disponibilidade, capacidade e localização.

#### Scenario: Visualização dos lares

- **WHEN** o administrador acessar o módulo
- **THEN** o sistema MUST apresentar os lares cadastrados, seus indicadores e os animais atualmente acolhidos.

#### Scenario: Filtragem dos lares

- **WHEN** o administrador selecionar um filtro
- **THEN** o sistema MUST apresentar somente os lares correspondentes ao critério selecionado.

#### Scenario: Consulta da ficha

- **WHEN** o administrador selecionar Ver Ficha
- **THEN** o sistema MUST apresentar as informações cadastradas do lar temporário.

### Requirement: Alocação de Animais

O sistema MUST permitir registrar a entrada de animais em lares temporários, respeitando a capacidade disponível e utilizando a entidade ANIMAL_LAR_TEMPORARIO.

#### Scenario: Alocação de animal

- **WHEN** o administrador selecionar um animal e um lar com vaga disponível
- **THEN** o sistema MUST registrar a entrada e a data de início da permanência.

#### Scenario: Capacidade máxima atingida

- **WHEN** o administrador tentar alocar um animal em um lar sem vagas
- **THEN** o sistema MUST impedir a alocação e informar a indisponibilidade.

### Requirement: Saída e Transferência de Animais

O sistema MUST permitir registrar a saída dos animais e preservar os registros de permanência anteriores.

#### Scenario: Encerramento da permanência

- **WHEN** o administrador registrar a saída de um animal
- **THEN** o sistema MUST registrar a data de encerramento da permanência.

#### Scenario: Transferência entre lares

- **WHEN** um animal for transferido para outro lar temporário
- **THEN** o sistema MUST encerrar a permanência anterior e registrar uma nova entrada, preservando o histórico.

### Requirement: Histórico de Acolhimento

O sistema MUST manter os registros de permanência dos animais nos lares temporários, incluindo datas de entrada, saída e observações.

#### Scenario: Consulta do histórico

- **WHEN** o administrador consultar o histórico de acolhimento
- **THEN** o sistema MUST apresentar os registros anteriores de permanência dos animais.