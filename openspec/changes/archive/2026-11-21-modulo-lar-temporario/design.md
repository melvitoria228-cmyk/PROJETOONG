# Design: Módulo de Lares Temporários

## Context

O módulo de **Lares Temporários** integra a Área Administrativa do **Porto Seguro Pet** (rota `/lares-temporarios`) e permite à equipe da ONG consultar a rede de residências acolhedoras, acompanhar a capacidade de vagas em tempo real e gerenciar as entradas, saídas e transferências dos animais resgatados.

A implementação utiliza as entidades existentes `LAR_TEMPORARIO`, `ANIMAL` e `ANIMAL_LAR_TEMPORARIO` no backend **Xano**, respeitando seus relacionamentos sem exigir alterações estruturais no banco de dados e compartilhando o menu lateral fixo `sidebar_administracao()` em `ProjetoONG.py`.

## Goals / Non-Goals

### Goals

- Disponibilizar a interface administrativa de Lares Temporários na rota `/lares-temporarios` com carregamento automático (`on_load`) e layout em **Grid de Cards de Capacidade**.
- Exibir indicadores resumidos de **lares ativos**, **vagas disponíveis** e **taxa de ocupação** calculados a partir dos registros vigentes.
- Permitir filtrar os lares por disponibilidade (`Todos`, `Com vagas`, `Capacidade máxima`) e buscar por texto no endereço cadastrado.
- Permitir consultar a ficha detalhada de cada lar (incluindo os animais atualmente acolhidos e o histórico completo de permanências anteriores com datas e observações).
- Permitir **alocar**, **encerrar permanência (saída)** e **transferir** animais entre lares temporários, respeitando o limite de capacidade e preservando todo o histórico em `ANIMAL_LAR_TEMPORARIO`.

### Non-Goals

- Criar novas colunas no banco de dados do Xano (como campo separado de bairro/região ou flag booleana de status ativo em `LAR_TEMPORARIO`).
- Excluir registros históricos de permanência já encerrados.
- Duplicar o componente de menu lateral fora de `sidebar_administracao()`.

## Decisions

### 1. Arquitetura Modular (`lares_temporarios_state.py` e `lares_temporarios.py`)

A implementação separa o gerenciamento de estado da camada de apresentação:
- **`ProjetoONG/lares_temporarios_state.py` (`LaresTemporariosState`):** armazena os lares, animais e registros de `ANIMAL_LAR_TEMPORARIO` carregados do Xano, calcula os indicadores de ocupação e vagas disponíveis por lar, aplica os filtros reativos e executa as operações de alocação, saída e transferência.
- **`ProjetoONG/lares_temporarios.py` (`pagina_lares_temporarios`):** renderiza o painel integrado ao `sidebar_administracao()`, contendo os cartões de métricas, barra de filtros, grid de cards de capacidade e modais de ficha/histórico, alocação e saída/transferência.
- **`ProjetoONG/ProjetoONG.py`:** registra a rota `/lares-temporarios` disparando o carregamento inicial no ciclo `on_load`.

### 2. Cálculo de Capacidade e Indicadores

- A ocupação atual de cada lar é calculada contando os registros em `ANIMAL_LAR_TEMPORARIO` vinculados ao lar que ainda não possuem `data_fim` preenchida.
- As vagas disponíveis correspondem à diferença entre a capacidade máxima cadastrada do lar e a quantidade de animais atualmente acolhidos.
- O sistema bloqueia novas alocações em lares cuja ocupação atingiu a capacidade máxima.
- O indicador de lares ativos é derivado diretamente dos registros disponíveis em `LAR_TEMPORARIO`, sem exigir novos campos na tabela.

### 3. Fluxo de Alocação, Saída e Transferência

- **Alocação:** cria um novo registro em `ANIMAL_LAR_TEMPORARIO` (`POST`) vinculando `animal_id` e `lar_temporario_id` com a data de início (`data_inicio`), impedindo alocação simultânea de um animal que já possua permanência aberta.
- **Saída:** atualiza o registro vigente (`PATCH`) preenchendo `data_fim` e eventuais observações de encerramento, preservando o registro no histórico.
- **Transferência:** encerra a permanência atual preenchendo `data_fim` (`PATCH`) e cria um novo registro de permanência (`POST`) no lar temporário de destino (desde que haja vaga disponível).

### 4. Localização e Histórico de Permanência

- O campo `endereco` cadastrado em `LAR_TEMPORARIO` é utilizado para exibir a localização nos cards e alimentar o filtro textual por região/bairro.
- A ficha do lar apresenta tanto os animais hospedados no momento quanto o histórico cronológico das permanências encerradas (`data_inicio`, `data_fim` e `observacoes`).

### 5. Integração Autenticada com o Xano e Identidade Visual

- Todas as requisições (`GET`, `POST`, `PATCH`) utilizam `httpx.AsyncClient` com token JWT (`Authorization: Bearer <token>` via `LoginState.token`) e URLs configuradas no `.env`, exibindo feedback ao usuário via `rx.toast`.
- A interface segue a paleta institucional da Área Administrativa (Areia `#EFE6DA`, Bege Claro `#F8F3EC`, Terracota `#A96348` / `#A65F43`, Verde Oliva `#737747` e Café Escuro `#2D1F18`).

## Risks / Trade-offs

- **Ausência de campo estruturado de bairro/região** → Mitigada utilizando busca textual flexível sobre o campo `endereco` já existente em `LAR_TEMPORARIO`.
- **Concorrência ou falha parcial durante transferência** → O fluxo executa o encerramento (`PATCH`) e a nova alocação (`POST`) em sequência validada, recarregando os dados do Xano e notificando via `rx.toast` em caso de falha.

## Migration Plan

1. Configurar as URLs dos endpoints de `LAR_TEMPORARIO`, `ANIMAL` e `ANIMAL_LAR_TEMPORARIO` no `.env`.
2. Implementar `LaresTemporariosState` em `ProjetoONG/lares_temporarios_state.py` e `pagina_lares_temporarios` em `ProjetoONG/lares_temporarios.py`.
3. Registrar a rota `/lares-temporarios` em `ProjetoONG/ProjetoONG.py` conectada ao `sidebar_administracao()` e ao evento `on_load`.
4. Validar os cálculos de capacidade, filtros de disponibilidade/localização, alocação, saída, transferência e consulta de histórico junto ao Xano.