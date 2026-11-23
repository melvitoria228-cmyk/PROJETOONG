# Proposal: Módulo de Lares Temporários

## Why

A equipe administrativa do **Porto Seguro Pet** precisa monitorar em tempo real a capacidade de acolhimento dos lares temporários, identificar quais animais resgatados estão alojados em cada residência e acompanhar a disponibilidade de vagas na rota `/lares-temporarios`.

Centralizar essas informações em uma interface conectada diretamente ao banco de dados facilita a alocação ágil de novos animais resgatados, garante o respeito ao limite de vagas de cada lar e preserva o histórico completo de entradas e saídas.

## What Changes

- Implementar a tela administrativa de **Lares Temporários** na rota `/lares-temporarios`, integrada ao menu lateral fixo (`sidebar_administracao`) em `ProjetoONG.py` com carregamento automático no `on_load` e layout em **Grid de Cards de Capacidade**.
- Apresentar indicadores resumidos no topo da tela: total de **lares ativos**, **vagas disponíveis** e **taxa de ocupação** geral da rede de acolhimento.
- Disponibilizar filtros rápidos para visualização de **todos os lares**, **lares com vagas disponíveis**, **lares com capacidade máxima** e busca por **localização (região ou bairro)**.
- Exibir os lares temporários em cartões contendo dados do responsável, localização, capacidade total, quantidade de animais acolhidos e identificação dos pets atualmente hospedados.
- Disponibilizar ações para consultar a ficha completa do lar temporário (incluindo o histórico de permanências anteriores e observações), **alocar um animal** em um lar com vaga disponível e **registrar a saída** do animal, preservando todo o histórico em `ANIMAL_LAR_TEMPORARIO`.
- Integrar todas as operações de consulta, alocação e encerramento de estadia aos endpoints autenticados do **Xano** via `httpx` com token JWT (`LoginState.token`) e feedback via `rx.toast`.

## Capabilities

### New Capabilities

- `gestao-lares-temporarios`: gerenciamento administrativo dos lares temporários na rota `/lares-temporarios`, visualização de capacidade e taxa de ocupação, filtros por disponibilidade/região, alocação e saída de animais e preservação do histórico de permanência integrado ao Xano.

### Modified Capabilities

Nenhuma.

## Impact

- **Frontend Reflex (`ProjetoONG/lares_temporarios_state.py` e `ProjetoONG/lares_temporarios.py`):** criação do estado `LaresTemporariosState` e da página `pagina_lares_temporarios` seguindo a paleta institucional da Área Administrativa.
- **Arquivo Principal (`ProjetoONG/ProjetoONG.py`):** registro da rota `/lares-temporarios` com disparo automático de carregamento no `on_load` e vinculação ao menu lateral unificado `sidebar_administracao()`.
- **Backend Xano:** consumo autenticado das entidades `LAR_TEMPORARIO`, `ANIMAL` e `ANIMAL_LAR_TEMPORARIO` (`GET`, `POST` e `PATCH`), respeitando o limite de capacidade de acolhimento e atualizando a situação do animal durante as movimentações.