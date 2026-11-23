# Design: Módulo de Doações

## Context

O módulo de **Doações** integra a Área Administrativa do **Porto Seguro Pet** (rota `/doacoes`) e tem como objetivo centralizar o cadastro de apoiadores e manter o histórico documental das contribuições financeiras e materiais recebidas pela ONG.

A interface é desenvolvida em **Python com Reflex** e comunica-se de forma assíncrona e autenticada via JWT com as entidades `DOADOR` e `DOACAO` no backend **Xano**, compartilhando a navegação lateral unificada `sidebar_administracao()` em `ProjetoONG.py`.

## Goals / Non-Goals

### Goals

- Disponibilizar a interface administrativa de Doações na rota `/doacoes` com carregamento automático (`on_load`).
- Apresentar indicadores resumidos de arrecadação financeira, doações materiais e total de doadores cadastrados.
- Permitir o cadastro e a consulta de doadores (`DOADOR`) integrados ao Xano.
- Permitir o registro (`POST`) e a consulta filtrada do histórico de doações (`DOACAO`), diferenciando contribuições financeiras e materiais.
- Identificar claramente o doador, o tipo, os detalhes da contribuição e a data de cada recebimento, com feedback via `rx.toast`.

### Non-Goals

- Implementar controle de estoque ou saldo disponível de insumos/materiais.
- Registrar baixas, consumos ou movimentações de saída de materiais.
- Gerenciar compras, fornecedores ou fluxo de caixa/conciliação bancária completa.
- Duplicar o componente de menu lateral fora de `sidebar_administracao()`.

## Decisions

### 1. Arquitetura Modular (`doacoes_state.py` e `doacoes.py`)

A implementação separa o gerenciamento de estado da camada visual:
- **`ProjetoONG/doacoes_state.py` (`DoacoesState`):** gerencia as listas de doadores e doações carregadas do Xano, os filtros de busca/tipo, os cálculos dos indicadores resumidos e os formulários/modais de cadastro de doador e registro de doação.
- **`ProjetoONG/doacoes.py` (`pagina_doacoes`):** estrutura a tela integrada ao `sidebar_administracao()`, exibindo os cartões de métricas, os filtros, o histórico de doações, a consulta de doadores e os modais de cadastro.
- **`ProjetoONG/ProjetoONG.py`:** registra a rota `/doacoes` disparando o carregamento inicial no ciclo `on_load`.

### 2. Tipos de Doação e Campos Condicionais

O sistema suporta dois tipos de registro na entidade `DOACAO`, alternando dinamicamente os campos do formulário conforme o tipo selecionado:
- **Financeira:** registra o valor recebido (`valor`), a forma de pagamento/observação e a data da doação, vinculados ao `doador_id`.
- **Material:** registra a descrição do item recebido (`descricao_item`), a quantidade/unidade e a data da doação, vinculados ao `doador_id` (com finalidade documental, sem controle de estoque).

### 3. Relacionamento entre Doadores e Doações

Um doador (`DOADOR`) pode realizar múltiplas doações (`DOACAO`) ao longo do tempo (relação `1:N`), enquanto cada registro de doação permanece obrigatoriamente vinculado a um único doador identificado na listagem.

### 4. Integração Autenticada com o Xano

As operações de consulta (`GET`) e gravação (`POST`) utilizam `httpx.AsyncClient` com o cabeçalho `Authorization: Bearer <token>` obtido de `LoginState.token` e URLs configuradas via variáveis de ambiente no `.env`. Após cada cadastro confirmado pelo servidor, as listas e os indicadores são atualizados imediatamente e o usuário recebe confirmação via `rx.toast`.

### 5. Identidade Visual Institucional

A página adota a paleta unificada da Área Administrativa (Areia `#EFE6DA`, Bege Claro `#F8F3EC`, Terracota `#A96348` / `#A65F43`, Verde Oliva `#737747` e Café Escuro `#2D1F18`), garantindo coerência visual com os demais módulos operacionais.

## Risks / Trade-offs

- **Ausência de controle de estoque** → Opção intencional de escopo; o sistema registra o histórico documental das entradas materiais sem rastrear consumo ou saldo em almoxarifado.
- **Dependência do cadastro prévio do doador** → Para registrar uma doação, o doador precisa estar selecionado; o fluxo mitiga atritos oferecendo cadastro rápido de novo doador diretamente na mesma tela.
- **Falha de comunicação ou validação no Xano** → Interceptadas com blocos `try/except`, mantendo o estado atual íntegro e exibindo alerta orientativo via `rx.toast`.

## Migration Plan

1. Configurar as URLs dos endpoints de `DOADOR` e `DOACAO` no `.env`.
2. Implementar `DoacoesState` em `ProjetoONG/doacoes_state.py` e `pagina_doacoes` em `ProjetoONG/doacoes.py`.
3. Registrar a rota `/doacoes` em `ProjetoONG/ProjetoONG.py` conectada ao `sidebar_administracao()` e ao evento `on_load`.
4. Validar o carregamento automático, o cadastro de doadores, o registro de doações financeiras e materiais, a filtragem do histórico e a persistência no Xano.