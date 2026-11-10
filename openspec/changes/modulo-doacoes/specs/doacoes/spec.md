# Capability: Doações

## ADDED Requirements

### Requirement: Cadastro de doadores

O sistema MUST permitir o cadastro dos dados dos doadores para identificação das pessoas que realizam doações à ONG.

#### Scenario: Cadastrar um doador

- WHEN o administrador preencher os dados obrigatórios de um novo doador
- THEN o sistema MUST registrar o doador.

#### Scenario: Consultar doadores cadastrados

- WHEN o administrador acessar a área de doadores
- THEN o sistema MUST apresentar os doadores cadastrados.

#### Scenario: CPF informado

- WHEN um CPF for informado no cadastro de um doador
- THEN o sistema MUST impedir o cadastro de outro doador com o mesmo CPF.

### Requirement: Registro de doações financeiras

O sistema MUST permitir o registro de doações financeiras recebidas pela ONG, vinculando cada registro a um doador.

#### Scenario: Registrar doação financeira

- WHEN o administrador selecionar o tipo financeira e informar o doador, o valor e a data da doação
- THEN o sistema MUST registrar a doação financeira vinculada ao doador selecionado.

#### Scenario: Consultar doações financeiras

- WHEN o administrador consultar o histórico de doações
- THEN o sistema MUST apresentar os registros de doações financeiras com seus respectivos valores e datas.

### Requirement: Registro de doações materiais

O sistema MUST permitir o registro de doações materiais recebidas pela ONG, vinculando cada registro a um doador.

#### Scenario: Registrar doação material

- WHEN o administrador selecionar o tipo material e informar o doador, a descrição do material e a data da doação
- THEN o sistema MUST registrar a doação material vinculada ao doador selecionado.

#### Scenario: Consultar doações materiais

- WHEN o administrador consultar o histórico de doações
- THEN o sistema MUST apresentar os registros de doações materiais com suas respectivas descrições e datas.

#### Scenario: Registrar material recebido

- WHEN uma doação material for registrada
- THEN o sistema MUST manter apenas o registro documental do recebimento, sem controlar quantidades disponíveis ou movimentações de estoque.

### Requirement: Histórico de doações

O sistema MUST manter o histórico das doações recebidas pela ONG, permitindo identificar o doador, o tipo e a data de cada doação.

#### Scenario: Consultar histórico

- WHEN o administrador acessar o histórico de doações
- THEN o sistema MUST apresentar os registros de doações financeiras e materiais.

#### Scenario: Consultar doações de um doador

- WHEN o administrador consultar as doações vinculadas a um doador
- THEN o sistema MUST apresentar os registros associados àquele doador.

### Requirement: Relacionamento entre doadores e doações

O sistema MUST permitir que um mesmo doador possua vários registros de doações, mantendo cada doação vinculada a um único doador.

#### Scenario: Doador realiza várias doações

- WHEN um doador realizar mais de uma doação ao longo do tempo
- THEN o sistema MUST manter cada doação como um registro independente, vinculado ao mesmo doador.
