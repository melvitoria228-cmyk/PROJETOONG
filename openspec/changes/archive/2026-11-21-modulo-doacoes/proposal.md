# Proposal: Módulo de Doações

## Why

A equipe administrativa do **Porto Seguro Pet** precisa centralizar, registrar e acompanhar as contribuições financeiras e materiais recebidas pela ONG, bem como manter um cadastro organizado dos doadores na rota `/doacoes`.

Sem um painel dedicado conectado ao banco de dados, os registros de arrecadação e itens doados ficam dispersos, dificultando a prestação de contas, o acompanhamento de entradas e o reconhecimento dos apoiadores.

## What Changes

- Implementar a interface administrativa de **Gestão de Doações** na rota `/doacoes`, integrada ao menu lateral fixo (`sidebar_administracao`) em `ProjetoONG.py` com carregamento automático no `on_load`.
- Disponibilizar indicadores resumidos (total arrecadado em dinheiro, quantidade de doações materiais e total de doadores ativos) e filtros de busca por doador, tipo de doação ou período.
- Permitir o cadastro e a consulta de **Doadores** (`DOADOR`: nome, tipo de pessoa/contato, telefone, e-mail e observações) diretamente integrados ao Xano.
- Permitir o registro e a consulta do histórico completo de **Doações** (`DOACAO`), diferenciando contribuições **Financeiras** (valor e forma de pagamento/comprovante) e **Materiais** (descrição do item e quantidade), sempre vinculadas ao doador e à data de recebimento.
- Integrar todas as operações de listagem (`GET`) e cadastro (`POST`) aos endpoints autenticados do **Xano** via `httpx` com token JWT (`LoginState.token`) e feedback imediato via `rx.toast`.

## Capabilities

### New Capabilities

- `doacoes`: gerenciamento administrativo de doadores (`DOADOR`), registro de doações financeiras e materiais (`DOACAO`), indicadores de arrecadação e consulta filtrada do histórico na rota `/doacoes` integrada ao Xano.

### Modified Capabilities

Nenhuma.

## Impact

- **Frontend Reflex (`ProjetoONG/doacoes_state.py` e `ProjetoONG/doacoes.py`):** criação do estado `DoacoesState` e da página `pagina_doacoes` seguindo a paleta institucional da Área Administrativa.
- **Arquivo Principal (`ProjetoONG/ProjetoONG.py`):** registro da rota `/doacoes` com carregamento automático no `on_load` e vinculação ao menu lateral unificado `sidebar_administracao()`.
- **Backend Xano:** consumo autenticado das entidades `DOADOR` e `DOACAO` (`GET` e `POST`) configuradas via variáveis de ambiente no `.env`.