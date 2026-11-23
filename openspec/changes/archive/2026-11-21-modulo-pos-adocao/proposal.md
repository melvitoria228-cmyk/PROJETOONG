# Proposal: Módulo de Pós-Adoção

## Why

Após a efetivação de uma adoção, a equipe administrativa do **Porto Seguro Pet** precisa acompanhar a adaptação do animal ao novo lar, verificar suas condições de bem-estar e registrar orientações repassadas ao tutor na rota `/pos-adocao`.

Sem uma visão cronológica dedicada a cada adoção concluída, os registros de acompanhamento ficam dispersos. Era necessário estruturar uma interface administrativa integrada ao backend **Xano** que apresentasse exclusivamente os processos com status `Adoção efetivada` e organizasse os registros de acompanhamento em uma **Linha do Tempo (Timeline)** decrescente.

## What Changes

- Implementar o módulo administrativo de **Pós-Adoção** na rota `/pos-adocao`, integrado ao menu lateral fixo (`sidebar_administracao`) em `ProjetoONG.py` com carregamento automático no `on_load`.
- Estruturar a tela no layout dividido em duas colunas (~30% / ~70%) seguindo a paleta institucional da Área Administrativa:
  - **Coluna Esquerda (~30%):** lista pesquisável/filtrável exibindo exclusivamente os processos de adoção com status `Adoção efetivada`, identificando o animal adotado e seu respectivo tutor.
  - **Coluna Direita (~70%):** cabeçalho resumido do animal e do tutor selecionados, formulário/modal para inclusão de novo acompanhamento (`POST`) e **Linha do Tempo (Timeline)** exibindo os registros vinculados em ordem cronológica decrescente (do mais recente para o mais antigo).
- Integrar todas as consultas (`GET`) e inclusões de acompanhamento (`POST` na entidade `ACOMPANHAMENTO_POS_ADOCAO`) aos endpoints autenticados do **Xano** via `httpx` com token JWT (`LoginState.token`) e feedback via `rx.toast`, utilizando estritamente os campos e relacionamentos existentes no banco de dados.

## Capabilities

### New Capabilities

- `pos-adocao`: acompanhamento administrativo pós-adoção na rota `/pos-adocao` em layout dividido (~30% / ~70%), filtragem exclusiva de processos com status `Adoção efetivada`, visualização cronológica decrescente em Linha do Tempo e registro de novos acompanhamentos integrados ao Xano.

### Modified Capabilities

Nenhuma.

## Impact

- **Frontend Reflex (`ProjetoONG/pos_adocao_state.py` e `ProjetoONG/pos_adocao.py`):** criação do estado `PosAdocaoState` e da interface `pagina_pos_adocao` alinhados à identidade visual da Área Administrativa.
- **Arquivo Principal (`ProjetoONG/ProjetoONG.py`):** registro da rota `/pos-adocao` com carregamento automático no `on_load` e vinculação ao menu lateral unificado `sidebar_administracao()`.
- **Backend Xano:** consumo autenticado das entidades `PROCESSO_ADOCAO`, `ANIMAL`, `TUTOR_ADOTANTE` e `ACOMPANHAMENTO_POS_ADOCAO` (`GET` e `POST`), sem criação de novos campos ou alteração nas tabelas existentes.