# Design: Módulo de Doações

## Context

O módulo de Doações fará parte da área administrativa do Porto Seguro Pet. Seu objetivo é organizar os dados dos doadores e manter o registro das doações financeiras e materiais recebidas pela ONG.

A interface será desenvolvida em Python com Reflex. A integração com o banco de dados Xano será realizada posteriormente.

## Goals / Non-Goals

### Goals

- Disponibilizar uma interface administrativa para Doações.
- Permitir o cadastro e a consulta de doadores.
- Permitir o registro de doações financeiras e materiais.
- Apresentar o histórico de doações recebidas.
- Identificar o doador, o tipo e a data de cada doação.

### Non-Goals

- Implementar controle de estoque.
- Controlar quantidades disponíveis de materiais.
- Registrar entradas e saídas de materiais.
- Gerenciar compras ou fornecedores.
- Implementar controle financeiro ou prestação de contas.

## Decisions

### 1. Organização da interface

A interface será acessada pelo menu administrativo por meio da opção Doações.

O módulo será organizado em áreas para:
- Consulta e cadastro de doadores.
- Registro de doações recebidas.
- Consulta do histórico de doações.

### 2. Tipos de doação

O sistema permitirá dois tipos de registro:

- **Financeira:** deverá registrar o valor recebido e a data da doação, vinculados ao doador.
- **Material:** deverá registrar a descrição do material recebido e a data da doação, vinculadas ao doador.

Os campos específicos serão apresentados conforme o tipo de doação selecionado.

### 3. Relacionamento entre doadores e doações

Um doador poderá realizar várias doações ao longo do tempo. Cada doação deverá estar vinculada a um único doador.

### 4. Organização dos dados

Serão utilizadas as entidades DOADOR e DOACAO, conforme o modelo de dados do projeto.

O registro de doações materiais terá finalidade exclusivamente documental, sem controle de estoque ou movimentações de materiais.

### 5. Integração com o banco de dados

Inicialmente, a interface será desenvolvida sem integração com o Xano. A conectividade será implementada em uma etapa posterior.

## Risks / Trade-offs

- A ausência de controle de estoque significa que o sistema não informará quantidades disponíveis de materiais recebidos.
- Os registros dependerão da identificação correta do doador e do preenchimento das informações correspondentes ao tipo de doação.

## Migration Plan

1. Criar a interface administrativa de Doações.
2. Criar a estrutura de estado do módulo.
3. Implementar os componentes de cadastro, registro e consulta.
4. Registrar a rota e integrar a opção ao menu administrativo.
5. Realizar a integração com o Xano posteriormente.
