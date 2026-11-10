# Change: Módulo de Doações

## Why

A ONG precisa organizar as informações dos doadores e das doações recebidas, evitando que esses registros fiquem descentralizados ou desorganizados.

## What Changes

- Criar uma interface administrativa para o gerenciamento de doações.
- Permitir o cadastro e a consulta de doadores.
- Permitir o registro de doações financeiras e materiais.
- Manter o histórico das doações recebidas, identificando o doador, o tipo e a data da doação.
- Permitir a consulta dos registros de doações.

## Capabilities

### New Capabilities

- `doacoes`: gerenciamento de doadores, registro de doações financeiras e materiais e consulta do histórico de recebimentos.

### Modified Capabilities

- Nenhuma.

## Impact

- Nova interface administrativa de Doações.
- Nova estrutura de estado para o módulo.
- Navegação administrativa e registro da rota correspondente.
- Entidades DOADOR e DOACAO no banco de dados Xano, cuja integração será realizada posteriormente.
