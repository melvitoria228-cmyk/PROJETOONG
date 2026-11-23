## Why

A ONG precisa organizar as informações dos animais resgatados em um local centralizado, permitindo que a equipe administrativa consulte, filtre e mantenha os registros atualizados de forma ágil. Esta mudança consolida o módulo de Gestão de Animais na rota dedicada `/animais`, integrando a interface Reflex diretamente à tabela `ANIMAL` no Xano e padronizando a experiência visual com o restante da Área Administrativa.

## What Changes

- Disponibilizar a tela administrativa de Gestão de Animais na rota dedicada `/animais`, integrada ao menu lateral fixo (`sidebar_administracao`) e seguindo a identidade visual institucional (paleta Terracota, Verde Oliva e Areia).
- Exibir cartões de resumo (KPIs) com total de animais cadastrados, quantidade de cães, quantidade de gatos e resgates realizados nos últimos 30 dias.
- Permitir consultar, buscar por nome/código, filtrar por espécie, porte e status, e navegar por paginação nos registros cadastrados.
- Permitir visualizar detalhes completos e ampliar a fotografia do animal (`foto_url`) por meio de modal interativo de imagem.
- Permitir cadastrar novos animais resgatados (`POST`) e editar seus registros (`PATCH`), com validação de campos obrigatórios e feedback visual via *toast*.
- Permitir excluir registros de animais (`DELETE`) mediante confirmação, respeitando as regras de integridade referencial e vínculos existentes.
- Integrar todas as operações da tela aos endpoints da tabela `ANIMAL` no Xano utilizando autenticação JWT (`LoginState.token`) e carregamento automático no ciclo de vida `on_load`.

## Capabilities

### New Capabilities

- `gestao-animais`: Consulta, indicadores resumidos, busca e filtros combinados, visualização detalhada com ampliação de foto (`foto_url`), cadastro, edição e exclusão de registros de animais na rota `/animais`, com integração autenticada ao Xano.

### Modified Capabilities

- `area-administrativa`: Registro da rota dedicada `/animais` conectada ao menu lateral fixo (`sidebar_administracao`).

## Impact

- **Frontend:** arquivos `gestao_animais.py` (interface, tabela, filtros e modais), `animais_state.py` (gerenciamento de estado e requisições assíncronas `httpx`) e `ProjetoONG.py` (registro da rota `/animais` e integração com `LoginState`).
- **Backend:** endpoints REST (`GET`, `POST`, `PATCH`, `DELETE`) da tabela `ANIMAL` no grupo de API `PortoSeguroPet` no Xano.
- **Dados:** campos (`codigo`, `nome`, `especie`, `sexo`, `raca`, `porte`, `idade_meses`, `data_resgate`, `saude`, `status`, `foto_url`) e integridade referencial com tabelas relacionadas (`PROCESSO_ADOCAO`, `ATENDIMENTO_VETERINARIO` e `ANIMAL_LAR_TEMPORARIO`).
- **Dependências:** utilização exclusiva dos componentes nativos do Reflex e `httpx` já presentes no projeto, sem introdução de dependências externas adicionais.