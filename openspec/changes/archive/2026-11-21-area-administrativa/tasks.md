## 1. Estrutura e Interface da Área Administrativa

- [x] 1.1 Criar a função `area_administrativa` e a rota `/administrativo` no frontend Reflex como painel institucional inicial.
- [x] 1.2 Implementar o componente unificado `sidebar_administracao()` (menu lateral permanentemente aberto) dividido nas seções PRINCIPAL, ATENDIMENTO e ADMINISTRAÇÃO com fundo Areia (`#EFE6DA`) e borda `#E2D7C7`.
- [x] 1.3 Adicionar a identificação da marca Porto Seguro Pet com ícone institucional e botão de encerramento de sessão (`LoginState.sair`).
- [x] 1.4 Organizar os itens do menu apontando para suas rotas dedicadas: Início (`/administrativo`), Gestão de Animais (`/animais`), Lares Temporários (`/lares-temporarios`), Atendimento Veterinário (`/atendimento-vet`), Adoções (`/adocoes`), Pós-Adoção (`/pos-adocao`), Voluntários (`/voluntarios`) e Doações (`/doacoes`).
- [x] 1.5 Construir o painel institucional inicial em `/administrativo` com cabeçalho animado (`/animais-boas-vindas.gif`) e grade de 5 cartões (*Quem somos*, *Nossa missão*, *Funcionalidades do sistema*, *Nosso público* e *Área do tutor*).
- [x] 1.6 Aplicar a paleta institucional unificada com fundo Bege Claro (`#F8F3EC`), Terracota (`#A96348` / `#A65F43`), Verde Oliva (`#737747`), Caramelo (`#8C6239`) e tipografia Café Escuro (`#2D1F18`).

## 2. Redirecionamento, Rotas e Controle de Acesso

- [x] 2.1 Garantir o direcionamento automático do usuário `administrador` para `/administrativo` após autenticação JWT no Xano.
- [x] 2.2 Impedir que usuários do tipo `Tutor/Adotante` acessem as rotas da Área Administrativa.
- [x] 2.3 Garantir que o encerramento de sessão (*logout*) limpe os dados da sessão local e redirecione o usuário para a tela inicial (`/`).
- [x] 2.4 Configurar os eventos `on_load` em cada rota dedicada para carregar automaticamente os dados do respectivo `State` junto ao Xano.

## 3. Módulo de Gestão de Animais (CRUD Completo)

- [x] 3.1 Desenvolver o módulo de Gestão de Animais em `gestao_animais.py` e `animais_state.py` na rota `/animais`, integrado à API do Xano via token JWT.
- [x] 3.2 Criar os cartões de resumo (total de cadastros, quantidade de cães, gatos e resgates nos últimos 30 dias).
- [x] 3.3 Implementar a barra de pesquisa por nome/código e filtros combinados por espécie, porte e status.
- [x] 3.4 Implementar a tabela de listagem exibindo avatar/foto do pet, informações gerais, status com badge colorida e botões de ação (Visualizar, Editar e Excluir).
- [x] 3.5 Implementar a paginação da tabela de animais.
- [x] 3.6 Criar os modais para visualização detalhada, criação (`POST`) e edição (`PATCH`) de registros de animais.
- [x] 3.7 Integrar a funcionalidade de exclusão de registros (`DELETE`) com diálogo de confirmação explícita e tratamento de integridade referencial.

## 4. Tratamento Visual de Fotos dos Animais

- [x] 4.1 Configurar o suporte à coluna de texto `foto_url` no Xano para armazenar links diretos de imagens dos pets.
- [x] 4.2 Desenvolver a extração e sanitização segura de URLs (`_extrair_url_foto`) com avatar neutro padronizado como *fallback* quando não houver URL válida.
- [x] 4.3 Adicionar pré-visualização da imagem no formulário de cadastro e edição.
- [x] 4.4 Implementar evento e modal `dialogo_foto_expandida` para exibição da foto em tamanho ampliado ao clicar nas miniaturas/avatars.

## 5. Integração dos Demais Módulos Operacionais e Validação Final

- [x] 5.1 Integrar os demais módulos do menu lateral (`LaresTemporariosState`, `AdocoesState`, `VoluntariosState`, `DoacoesState` e atendimento/pós-adoção) às respectivas rotas dedicadas e endpoints do Xano.
- [x] 5.2 Testar as requisições de consulta, criação, edição e exclusão com o backend Xano, incluindo cenários de erro e validações.
- [x] 5.3 Testar a navegação entre todas as rotas da Área Administrativa e a abertura/fechamento dos modais em diferentes resoluções.
- [x] 5.4 Executar compilação do projeto e confirmar a ausência de erros de sintaxe ou conflitos de rota nos arquivos da aplicação.