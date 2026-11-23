# Tasks: Módulo de Voluntários

## 1. Estrutura Modular e Estado (`ProjetoONG/voluntarios_state.py`)

- [x] 1.1 Criar o arquivo de estado `ProjetoONG/voluntarios_state.py` (`VoluntariosState`) para gerenciar voluntários, atividades, vínculos de participação e filtros.
- [x] 1.2 Implementar os getters reativos para cálculo dos indicadores resumidos (total de voluntários, total de atividades e total de participações) e filtragem bidirecional do histórico.
- [x] 1.3 Definir o mapeamento das entidades `VOLUNTARIO`, `ATIVIDADE` e da tabela associativa `VOLUNTARIO_ATIVIDADE` (`N:N`), incluindo validação preventiva contra vínculos duplicados na mesma atividade.

## 2. Interface Administrativa (`ProjetoONG/voluntarios.py` / `tela_voluntarios.py`)

- [x] 2.1 Criar a página administrativa de Voluntários integrada ao menu lateral fixo `sidebar_administracao()` e à paleta institucional da Área Administrativa (Areia, Bege Claro, Terracota e Verde Oliva).
- [x] 2.2 Exibir os cartões de indicadores resumidos e os filtros de busca por nome do voluntário, disponibilidade/habilidade ou atividade.
- [x] 2.3 Implementar a área e o formulário/modal de cadastro e consulta de voluntários (`VOLUNTARIO`).
- [x] 2.4 Implementar a área e o formulário/modal de registro e consulta de atividades (`ATIVIDADE`).
- [x] 2.5 Implementar a área de associação entre voluntários e atividades (`VOLUNTARIO_ATIVIDADE`) e a consulta do histórico bidirecional (atividades por voluntário e participantes por atividade).

## 3. Integração Autenticada com o Xano (`ProjetoONG/voluntarios_state.py`)

- [x] 3.1 Configurar a leitura das URLs dos endpoints de `VOLUNTARIO`, `ATIVIDADE` e `VOLUNTARIO_ATIVIDADE` via `.env`.
- [x] 3.2 Implementar o carregamento assíncrono (`httpx` + token JWT `LoginState.token`) das listas de voluntários, atividades e participações vinculadas.
- [x] 3.3 Integrar o cadastro de voluntários (`POST`), o registro de atividades (`POST`) e a vinculação de participações (`POST`) ao Xano com atualização imediata da interface e feedback via `rx.toast`.

## 4. Navegação, Roteamento e Validação (`ProjetoONG/ProjetoONG.py`)

- [x] 4.1 Garantir a opção "Voluntários" no menu lateral unificado `sidebar_administracao()`.
- [x] 4.2 Registrar a rota `/voluntarios` em `ProjetoONG/ProjetoONG.py` com carregamento automático no ciclo `on_load`.
- [x] 4.3 Testar o cadastro de voluntários e atividades, a prevenção de vínculos duplicados, a consulta bidirecional do histórico e validar a change com `openspec validate`.