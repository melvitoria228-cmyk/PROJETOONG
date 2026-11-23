## 1. Conferir a estrutura existente

- [x] 1.1 Inspecionar a implementação de `ProjetoONG.py` e definir a arquitetura modular da Área Administrativa com menu lateral fixo (`sidebar_administracao`) e rotas dedicadas.
- [x] 1.2 Conferir os endpoints REST (`GET`, `POST`, `PATCH`, `DELETE`) da tabela `ANIMAL` no grupo de API `PortoSeguroPet` no Xano.
- [x] 1.3 Confirmar os campos (`nome`, `especie`, `raca`, `idade_estimada`, `sexo`, `porte`, `condicao_saude`, `status_atual`, `data_resgate` e `foto_url`), tipos, obrigatoriedade e opções padronizadas aceitas pelo Xano.

## 2. Preparar a integração e o estado (`animais_state.py`)

- [x] 2.1 Configurar a variável de ambiente `XANO_ANIMAL_URL` no `.env` e reutilizar o token JWT da sessão (`LoginState.token`) nas requisições `httpx` assíncronas.
- [x] 2.2 Implementar no `AnimaisState` as operações de consulta, cadastro, edição e exclusão usando os endpoints existentes do Xano.
- [x] 2.3 Implementar a lógica de filtros combinados (busca textual, espécie, porte e status), paginação e cálculo dos indicadores resumidos (KPIs).
- [x] 2.4 Tratar erros HTTP, falhas de comunicação e bloqueios de integridade referencial do Xano com notificações *toast*, sem apresentar operações malsucedidas como concluídas.

## 3. Construir a estrutura visual da tela (`gestao_animais.py`)

- [x] 3.1 Criar o layout principal da página em duas colunas integrando o menu lateral fixo (`sidebar_administracao`) e a área de conteúdo com cabeçalho e botão de novo cadastro.
- [x] 3.2 Construir os cartões de indicadores resumidos (total de registros, cães, gatos e resgates nos últimos 30 dias) e a barra de busca e filtros combinados.
- [x] 3.3 Construir a tabela responsiva de listagem com miniatura/avatar do pet, colunas padronizadas, badges de status e controles de paginação.
- [x] 3.4 Criar os modais da tela: visualização detalhada do animal, ampliação de fotografia (`foto_url`), formulário de cadastro/edição e diálogo de confirmação de exclusão.
- [x] 3.5 Registrar a rota dedicada `/animais` em `ProjetoONG.py` com carregamento automático (`on_load`) e aplicar a paleta institucional (Terracota, Verde Oliva e Areia).

## 4. Implementar os fluxos operacionais (CRUD e visualização)

- [x] 4.1 Conectar a listagem da tabela aos dados retornados pelo Xano, contemplando estados de carregamento, lista vazia e erro.
- [x] 4.2 Conectar a visualização detalhada do registro e a abertura do modal de ampliação de foto ao clicar na miniatura (com avatar neutro como *fallback*).
- [x] 4.3 Conectar o formulário de cadastro (`POST`) com validação de campos obrigatórios e atualização da lista após confirmação do backend.
- [x] 4.4 Conectar o formulário de edição (`PATCH`) com preenchimento automático dos dados atuais e atualização da lista após confirmação do backend.
- [x] 4.5 Conectar a exclusão (`DELETE`) ao modal de confirmação explícita e tratar bloqueios por relacionamentos ativos (`PROCESSO_ADOCAO`, `ATENDIMENTO_VETERINARIO` e `ANIMAL_LAR_TEMPORARIO`).

## 5. Validar a implementação

- [x] 5.1 Testar consulta, KPIs, busca/filtros, paginação, visualização com ampliação de foto, cadastro, edição e exclusão, incluindo validações e cenários de falha.
- [x] 5.2 Executar a validação do OpenSpec e verificar se o login, as demais rotas administrativas (`/administrativo`, `/lares-temporarios`, `/atendimento-vet`, `/adocoes`, `/pos-adocao`, `/voluntarios`, `/doacoes`) e a Área do Tutor (`/tutor`) permanecem funcionando integralmente.