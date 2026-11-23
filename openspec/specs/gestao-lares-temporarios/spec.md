# gestao-lares-temporarios Specification

## Purpose
Definir os requisitos funcionais do módulo administrativo de **Lares Temporários** na rota `/lares-temporarios`, permitindo monitorar a capacidade e a ocupação da rede de acolhimento, filtrar residências por disponibilidade e localização, gerenciar alocações, saídas e transferências de animais e consultar o histórico completo de permanências integrado ao backend Xano.

## Requirements

### Requirement: Visualização, Carregamento Automático e Consulta dos Lares Temporários

O sistema MUST carregar automaticamente os dados de `LAR_TEMPORARIO`, `ANIMAL` e `ANIMAL_LAR_TEMPORARIO` no `on_load` da rota `/lares-temporarios` (via token JWT do Xano), apresentar indicadores resumidos de ocupação e exibir os lares temporários em cards com responsável, endereço, capacidade e quantidade de animais acolhidos.

#### Scenario: Visualização dos lares e indicadores

- **WHEN** o administrador acessar a rota `/lares-temporarios`
- **THEN** o sistema MUST carregar os registros autenticados do Xano, calcular os indicadores resumidos (lares ativos, vagas disponíveis e taxa de ocupação) e apresentar os cards dos lares com os animais atualmente acolhidos (registros sem `data_fim`).

#### Scenario: Filtragem dos lares por disponibilidade e localização

- **WHEN** o administrador selecionar um filtro de disponibilidade (`Todos`, `Com vagas`, `Capacidade máxima`) ou informar um termo de busca no endereço
- **THEN** o sistema MUST atualizar a listagem exibindo apenas os lares correspondentes aos critérios selecionados.

#### Scenario: Consulta da ficha do lar temporário

- **WHEN** o administrador selecionar a ação de consultar a ficha ("Ver Ficha") de um lar temporário
- **THEN** o sistema MUST apresentar os dados cadastrais completos do lar, os animais atualmente alojados e o histórico de permanências anteriores.

#### Scenario: Falha de comunicação com o backend

- **WHEN** ocorrer erro de rede ou rejeição na consulta ou gravação junto ao Xano
- **THEN** o sistema MUST preservar o estado atual da interface e notificar o usuário via *toast*.

### Requirement: Alocação de Animais

O sistema MUST permitir registrar a entrada de animais em lares temporários (`POST` em `ANIMAL_LAR_TEMPORARIO`), respeitando a capacidade máxima disponível de cada lar.

#### Scenario: Alocação de animal com vaga disponível

- **WHEN** o administrador selecionar um animal elegível e um lar temporário com vaga disponível e confirmar a alocação
- **THEN** o sistema MUST registrar a entrada no Xano com a data de início (`data_inicio`), recalcular a ocupação do lar e exibir confirmação via *toast*.

#### Scenario: Capacidade máxima atingida

- **WHEN** o administrador tentar alocar um animal em um lar cuja ocupação atual já atingiu a capacidade máxima
- **THEN** o sistema MUST impedir a alocação e informar a indisponibilidade de vagas.

### Requirement: Saída e Transferência de Animais

O sistema MUST permitir registrar a saída ou a transferência de animais acolhidos, preservando os registros de permanência anteriores.

#### Scenario: Encerramento da permanência (Saída)

- **WHEN** o administrador registrar a saída de um animal de um lar temporário
- **THEN** o sistema MUST atualizar o registro vigente (`PATCH` em `ANIMAL_LAR_TEMPORARIO`) preenchendo a data de encerramento (`data_fim`) e eventuais observações, liberando a vaga no lar e exibindo confirmação via *toast*.

#### Scenario: Transferência entre lares temporários

- **WHEN** um animal for transferido para outro lar temporário com vaga disponível
- **THEN** o sistema MUST encerrar a permanência anterior (`data_fim`) e criar um novo registro de entrada (`POST`) no lar de destino, preservando integralmente o histórico de ambas as estadias.

### Requirement: Histórico de Acolhimento

O sistema MUST manter e exibir os registros históricos de permanência dos animais nos lares temporários, incluindo datas de entrada (`data_inicio`), saída (`data_fim`) e observações.

#### Scenario: Consulta do histórico de permanências

- **WHEN** o administrador consultar o histórico de acolhimento na ficha de um lar temporário
- **THEN** o sistema MUST apresentar os registros anteriores de permanência em ordem cronológica com identificação do animal, datas de início e encerramento e observações registradas.
