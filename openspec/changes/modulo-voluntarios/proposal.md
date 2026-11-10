# Change: Módulo de Voluntários

## Why

A ONG precisa organizar as informações dos voluntários e registrar suas participações nas atividades, evitando que esses dados fiquem descentralizados ou desorganizados.

## What Changes

- Criar uma interface administrativa para o gerenciamento de voluntários.
- Permitir o cadastro e a consulta de voluntários.
- Permitir o registro e a consulta de atividades.
- Associar voluntários às atividades das quais participam.
- Manter o histórico de participação dos voluntários.

## Capabilities

### New Capabilities

- `voluntarios`: gerenciamento de voluntários, registro de atividades e acompanhamento das participações.

### Modified Capabilities

- Nenhuma.

## Impact

- Nova interface administrativa de Voluntários.
- Nova estrutura de estado para o módulo.
- Navegação administrativa e registro da rota correspondente.
- Entidades VOLUNTARIO, ATIVIDADE e VOLUNTARIO_ATIVIDADE no banco de dados Xano, cuja integração será realizada posteriormente.
