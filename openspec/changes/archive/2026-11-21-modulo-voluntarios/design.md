# Design: Módulo de Voluntários

## Context

O módulo de **Voluntários** integra a Área Administrativa do **Porto Seguro Pet** (rota `/voluntarios`) e tem como objetivo centralizar o cadastro de voluntários, organizar as atividades operacionais e eventos da ONG e manter o histórico de participação de cada colaborador.

A interface é desenvolvida em **Python com Reflex** e comunica-se de forma assíncrona e autenticada via JWT com as entidades `VOLUNTARIO`, `ATIVIDADE` e `VOLUNTARIO_ATIVIDADE` no backend **Xano**, compartilhando o menu lateral fixo `sidebar_administracao()` em `ProjetoONG.py`.

## Goals / Non-Goals

### Goals

- Disponibilizar a interface administrativa de Voluntários na rota `/voluntarios` com carregamento automático (`on_load`).
- Apresentar indicadores resumidos de voluntários cadastrados, atividades registradas e participações vinculadas.
- Permitir o cadastro (`POST`) e a consulta filtrada (`GET`) de voluntários (`VOLUNTARIO`).
- Permitir o registro (`POST`) e a consulta (`GET`) de atividades da ONG (`ATIVIDADE`).
- Permitir associar voluntários às atividades por meio da entidade associativa `VOLUNTARIO_ATIVIDADE`, impedindo vínculos duplicados na mesma atividade e preservando o histórico de participações.

### Non-Goals

- Implementar controle de pagamentos, ajuda de custo ou remuneração.
- Gerenciar escalas complexas de turnos ou quadro de horários recorrentes.
- Implementar controle de ponto biométrico, folha de frequência ou cálculo de horas trabalhadas.
- Implementar fluxo público de recrutamento ou triagem de candidatos externos.
- Duplicar o componente de menu lateral fora de `sidebar_administracao()`.

## Decisions

### 1. Arquitetura Modular (`voluntarios_state.py` e `voluntarios.py`)

A implementação separa o gerenciamento de estado da camada de apresentação:
- **`ProjetoONG/voluntarios_state.py` (`VoluntariosState`):** armazena as listas de voluntários, atividades e vínculos de participação carregados do Xano, calcula os indicadores resumidos, aplica filtros de pesquisa e executa os cadastros e associações (`POST`).
- **`ProjetoONG/voluntarios.py` (`pagina_voluntarios`):** estrutura a tela integrada ao `sidebar_administracao()`, exibindo os cartões de métricas, os filtros, as áreas de consulta/cadastro de voluntários e atividades, o vínculo de participação e o histórico consolidado.
- **`ProjetoONG/ProjetoONG.py`:** registra a rota `/voluntarios` disparando o carregamento inicial no ciclo `on_load`.

### 2. Relacionamento `N:N` via `VOLUNTARIO_ATIVIDADE`

- Um voluntário (`VOLUNTARIO`) pode participar de múltiplas atividades (`ATIVIDADE`) ao longo do tempo, e uma atividade pode contar com vários voluntários simultaneamente.
- A entidade associativa `VOLUNTARIO_ATIVIDADE` materializa cada participação vinculando `voluntario_id` e `atividade_id` (além de observações/função desempenhada, quando disponíveis).
- Antes de efetivar uma nova associação, o estado valida se o par `(voluntario_id, atividade_id)` já existe, impedindo registros redundantes para a mesma atividade.

### 3. Consulta e Filtragem do Histórico

- A interface permite pesquisar voluntários por nome, disponibilidade ou habilidade, bem como filtrar participações por voluntário específico ou por atividade, facilitando a montagem de equipes para novos eventos.

### 4. Integração Autenticada com o Xano e Identidade Visual

- Todas as requisições (`GET` e `POST`) utilizam `httpx.AsyncClient` com o cabeçalho `Authorization: Bearer <token>` obtido de `LoginState.token` e URLs configuradas no `.env`, exibindo confirmações e alertas via `rx.toast`.
- A interface adota a paleta institucional da Área Administrativa (Areia `#EFE6DA`, Bege Claro `#F8F3EC`, Terracota `#A96348` / `#A65F43`, Verde Oliva `#737747` e Café Escuro `#2D1F18`).

## Risks / Trade-offs

- **Ausência de controle de ponto ou carga horária** → Opção intencional de escopo; o sistema registra a participação documental nas atividades sem calcular horas acumuladas.
- **Vínculos duplicados entre o mesmo voluntário e atividade** → Mitigados por validação preventiva no `VoluntariosState` antes do envio (`POST`) ao Xano.
- **Falha de comunicação com o backend** → Tratada com blocos `try/except`, mantendo o estado atual íntegro e exibindo aviso orientativo via `rx.toast`.

## Migration Plan

1. Configurar as URLs dos endpoints de `VOLUNTARIO`, `ATIVIDADE` e `VOLUNTARIO_ATIVIDADE` no `.env`.
2. Implementar `VoluntariosState` em `ProjetoONG/voluntarios_state.py` e `pagina_voluntarios` em `ProjetoONG/voluntarios.py`.
3. Registrar a rota `/voluntarios` em `ProjetoONG/ProjetoONG.py` conectada ao `sidebar_administracao()` e ao evento `on_load`.
4. Validar o carregamento automático, o cadastro de voluntários e atividades, a prevenção de vínculos duplicados e a consulta do histórico junto ao Xano.