# Spec: Módulo de Doações

## Purpose

Definir os requisitos funcionais do módulo administrativo de **Doações** na rota `/doacoes`, permitindo cadastrar e consultar doadores (`DOADOR`), registrar contribuições financeiras e materiais (`DOACAO`), visualizar indicadores resumidos e consultar o histórico completo integrado ao backend Xano.

## ADDED Requirements

### Requirement: Carregamento Automático e Indicadores de Arrecadação

O sistema MUST carregar automaticamente os dados de doadores e doações no `on_load` da rota `/doacoes` (via token JWT do Xano) e exibir indicadores resumidos de arrecadação.

#### Scenario: Carregar painel de doações com sucesso
- **WHEN** o administrador acessar a rota `/doacoes`
- **THEN** o sistema MUST consultar os registros autenticados de `DOADOR` e `DOACAO` no Xano, calcular os indicadores resumidos (total financeiro arrecadado, quantidade de doações materiais e total de doadores) e exibir o histórico na interface.

#### Scenario: Falha de comunicação com o backend
- **WHEN** ocorrer erro de rede ou rejeição na consulta ou cadastro junto ao Xano
- **THEN** o sistema MUST preservar o estado atual da interface e notificar o usuário via *toast*.

### Requirement: Cadastro e Consulta de Doadores

O sistema MUST permitir o cadastro (`POST`) e a consulta (`GET`) dos dados dos doadores (`DOADOR`) integrados ao Xano para identificação dos apoiadores da ONG.

#### Scenario: Cadastrar um novo doador
- **WHEN** o administrador preencher os dados obrigatórios de um novo doador e confirmar o envio
- **THEN** o sistema MUST registrar o doador no Xano, atualizar a listagem disponível para vínculo de doações e exibir confirmação via *toast*.

#### Scenario: Consultar doadores cadastrados
- **WHEN** o administrador acessar a área ou seletor de doadores
- **THEN** o sistema MUST apresentar os doadores cadastrados com suas informações de identificação e contato.

#### Scenario: Impedir duplicidade de CPF
- **WHEN** um CPF já cadastrado for informado no registro de um novo doador
- **THEN** o sistema MUST impedir o cadastro duplicado e exibir alerta orientativo via *toast*.

### Requirement: Registro de Doações Financeiras

O sistema MUST permitir o registro de doações financeiras recebidas pela ONG (`POST` em `DOACAO`), vinculando cada registro a um doador cadastrado.

#### Scenario: Registrar doação financeira
- **WHEN** o administrador selecionar o tipo `Financeira` e informar o doador, o valor e a data da doação
- **THEN** o sistema MUST registrar a doação financeira vinculada ao `doador_id` no Xano, recalcular o total arrecadado e exibir confirmação via *toast*.

#### Scenario: Consultar doações financeiras
- **WHEN** o administrador consultar o histórico de doações
- **THEN** o sistema MUST apresentar os registros de doações financeiras com identificação do doador, valor formatado e data de recebimento.

### Requirement: Registro de Doações Materiais

O sistema MUST permitir o registro documental de doações materiais recebidas pela ONG (`POST` em `DOACAO`), vinculando cada registro a um doador cadastrado.

#### Scenario: Registrar doação material
- **WHEN** o administrador selecionar o tipo `Material` e informar o doador, a descrição do material e a data da doação
- **THEN** o sistema MUST registrar a doação material vinculada ao `doador_id` no Xano e exibir confirmação via *toast*.

#### Scenario: Consultar doações materiais sem controle de estoque
- **WHEN** uma doação material for registrada e consultada no histórico
- **THEN** o sistema MUST apresentar sua descrição, quantidade informada e data apenas como registro documental de recebimento, sem controlar saldos disponíveis ou movimentações de saída de estoque.

### Requirement: Histórico Filtrado e Relacionamento entre Doadores e Doações

O sistema MUST manter o histórico unificado das doações recebidas (relação `1:N` entre `DOADOR` e `DOACAO`), permitindo filtrar e consultar contribuições por doador ou tipo.

#### Scenario: Consultar e filtrar histórico de doações
- **WHEN** o administrador acessar o histórico ou aplicar filtros por nome do doador ou tipo de doação (`Financeira` / `Material`)
- **THEN** o sistema MUST atualizar a listagem exibindo os registros correspondentes com doador, tipo, detalhes e data.

#### Scenario: Doador realiza múltiplas doações
- **WHEN** um mesmo doador realizar mais de uma doação ao longo do tempo
- **THEN** o sistema MUST manter cada doação como um registro independente vinculado ao mesmo doador no histórico.