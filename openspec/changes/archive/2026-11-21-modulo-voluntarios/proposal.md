# Proposal: Módulo de Voluntários

## Why

A equipe administrativa do **Porto Seguro Pet** precisa centralizar o cadastro de colaboradores voluntários, organizar as atividades operacionais e eventos da ONG e registrar a participação de cada voluntário na rota `/voluntarios`.

Sem um painel dedicado conectado ao banco de dados, as informações de disponibilidade, habilidades e histórico de engajamento ficam dispersas, dificultando a escalação de equipes para mutirões, feiras de adoção, resgates e apoio interno.

## What Changes

- Implementar a interface administrativa de **Gestão de Voluntários** na rota `/voluntarios`, integrada ao menu lateral fixo (`sidebar_administracao`) em `ProjetoONG.py` com carregamento automático no `on_load`.
- Apresentar indicadores resumidos (total de voluntários cadastrados, atividades registradas e participações vinculadas) e filtros de busca por nome, disponibilidade ou atividade.
- Permitir o cadastro e a consulta de **Voluntários** (`VOLUNTARIO`: nome, telefone, e-mail, disponibilidade e habilidades/área de atuação) integrados ao Xano.
- Permitir o registro e a consulta de **Atividades** (`ATIVIDADE`: título/nome da atividade, data, descrição e local/observações) integrados ao Xano.
- Permitir associar voluntários às atividades (`VOLUNTARIO_ATIVIDADE`), evitando vínculos duplicados na mesma atividade e mantendo o histórico completo de participações por voluntário e por evento.
- Integrar todas as operações de consulta (`GET`) e cadastro/vinculação (`POST`) aos endpoints autenticados do **Xano** via `httpx` com token JWT (`LoginState.token`) e feedback imediato via `rx.toast`.

## Capabilities

### New Capabilities

- `voluntarios`: gerenciamento administrativo de voluntários (`VOLUNTARIO`), registro de atividades (`ATIVIDADE`), vinculação de participações (`VOLUNTARIO_ATIVIDADE`) e consulta do histórico na rota `/voluntarios` integrado ao Xano.

### Modified Capabilities

Nenhuma.

## Impact

- **Frontend Reflex (`ProjetoONG/voluntarios_state.py` e `ProjetoONG/voluntarios.py`):** criação do estado `VoluntariosState` e da página `pagina_voluntarios` seguindo a paleta institucional da Área Administrativa.
- **Arquivo Principal (`ProjetoONG/ProjetoONG.py`):** registro da rota `/voluntarios` com carregamento automático no `on_load` e vinculação ao menu lateral unificado `sidebar_administracao()`.
- **Backend Xano:** consumo autenticado das entidades `VOLUNTARIO`, `ATIVIDADE` e `VOLUNTARIO_ATIVIDADE` (`GET` e `POST`) configuradas via variáveis de ambiente no `.env`.