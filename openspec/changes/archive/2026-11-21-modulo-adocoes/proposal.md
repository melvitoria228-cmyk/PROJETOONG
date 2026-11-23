# Proposal: Módulo de Adoções

## Why

A equipe administrativa do **Porto Seguro Pet** precisa analisar, triar e conduzir os processos de adoção de forma organizada, ágil e auditável na rota `/adocoes`.

Para apoiar a tomada de decisão dos administradores, é essencial visualizar lado a lado a fila de solicitações e o dossiê completo de cada candidatura (dados do animal resgatado, perfil do tutor/adotante e questionário de triagem), garantindo que informações sensíveis e respostas declaradas não sejam adulteradas durante a análise, ao mesmo tempo em que permite atualizar contatos e avançar o status do processo diretamente no backend Xano.

## What Changes

- Implementar o módulo administrativo de Gestão de Adoções na rota `/adocoes` integrado ao menu lateral fixo (`sidebar_administracao`) em `ProjetoONG.py`, com carregamento automático via `on_load`.
- Organizar a interface no padrão **Master-Detail** (~35% / ~65%):
  - **Painel Master (Esquerda):** listagem das solicitações de adoção com busca por nome do solicitante ou animal e filtro por status do processo (`Em análise`, `Aprovada`, `Adoção efetivada`, `Recusada`, etc.).
  - **Painel Detail (Direita):** exibição detalhada do pet solicitado (nome, espécie, porte, status), dados cadastrais do tutor/adotante e respostas do questionário de triagem.
- Garantir a auditabilidade do processo mantendo campos sensíveis (como CPF e respostas do questionário) bloqueados para edição (somente leitura), permitindo apenas a atualização controlada de dados de contato do tutor por meio de modal dedicado.
- Integrar a consulta, atualização de status do processo de adoção e atualização de contato do tutor aos endpoints autenticados do **Xano** (`PROCESSO_ADOCAO`, `TUTOR_ADOTANTE` e `ANIMAL`) via requisições assíncronas (`httpx`) com token JWT (`LoginState.token`) e feedback via `rx.toast`.

## Capabilities

### New Capabilities

- `gestao-adocoes-admin`: gerenciamento administrativo dos processos de adoção em layout Master-Detail na rota `/adocoes`, incluindo busca/filtros, triagem auditável com bloqueio de campos sensíveis, edição controlada de contato via modal e atualização de status integrada ao Xano.

### Modified Capabilities

Nenhuma.

## Impact

- **Frontend Reflex (`ProjetoONG/adocoes.py` e `ProjetoONG/animais_state.py` / `adocoes_state.py`):** criação da página `pagina_adocoes` em layout Master-Detail, modais de edição de contato/status e gerenciamento de estado `AdocoesState`.
- **Arquivo Principal (`ProjetoONG/ProjetoONG.py`):** registro da rota `/adocoes` com disparo automático de carregamento no `on_load` e vinculação ao menu lateral unificado `sidebar_administracao()`.
- **Backend Xano:** consumo autenticado dos endpoints de `PROCESSO_ADOCAO` (com dados relacionados de `ANIMAL` e `TUTOR_ADOTANTE`) e `PATCH` para atualização de status da adoção e contato do tutor.