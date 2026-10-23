## 1. Estrutura e Interface da Área Administrativa

- [x] 1.1 Criar a função e a rota `/administrativo` no frontend Reflex para a Área Administrativa.
- [x] 1.2 Implementar o menu lateral fixo (sempre aberto) dividido nas seções PRINCIPAL, ATENDIMENTO e ADMINISTRAÇÃO com fundo `#F4E7D5`.
- [x] 1.3 Adicionar a identificação da marca Porto Seguro Pet com ícone institucional e atalho de saída (*logout*).
- [x] 1.4 Organizar os itens do menu (Início, Gestão de Animais, Lares Temporários, Atendimento Veterinário, Adoções, Pós-Adoção, Voluntários, Estoque, Doações).
- [x] 1.5 Aplicar a paleta institucional com grafite (`#342D29` / `#3E4149`), creme (`#FAF6F0` / `#F4E7D5`) e terracota (`#684638` / `#D78A45`).
- [x] 1.6 Implementar a seleção dinâmica de telas no menu lateral através de `LoginState.tela_atual`.

## 2. Redirecionamento e Controle de Acesso

- [x] 2.1 Verificar o direcionamento automático do usuário `administrador` para `/administrativo` após autenticação no Xano.
- [x] 2.2 Impedir que usuários do tipo `Tutor/Adotante` acessem a Área Administrativa.
- [x] 2.3 Garantir que o encerramento de sessão (*logout*) limpe os dados da sessão e redirecione o usuário de volta para a tela inicial `/`.

## 3. Módulo de Gestão de Animais (CRUD Completo)

- [x] 3.1 Desenvolver o módulo de Gestão de Animais em `gestao_animal.py` integrado à API do Xano via token JWT.
- [x] 3.2 Criar os cartões de resumo (total de cadastros, quantidade de cães, gatos e resgates nos últimos 30 dias).
- [x] 3.3 Implementar a barra de pesquisa por nome/código e filtros por espécie, porte e status.
- [x] 3.4 Implementar a tabela de listagem exibindo avatar/foto do pet, informações gerais, status com badge colorida e botões de ação (Visualizar, Editar e Excluir).
- [x] 3.5 Implementar a paginação da tabela de animais.
- [x] 3.6 Criar o formulário em modal para criação (`POST`) e edição (`PATCH`) de registros de animais.
- [x] 3.7 Integrar a funcionalidade de exclusão de registros (`DELETE`) com diálogo de confirmação.

## 4. Tratamento Visual de Fotos dos Animais

- [x] 4.1 Configurar o suporte à coluna de texto `foto_url` no Xano para armazenar links diretos de imagens dos pets.
- [x] 4.2 Desenvolver a extração e sanitização segura de URLs (`_extrair_url_foto`) com imagem fallback quando não houver URL válida.
- [x] 4.3 Adicionar pré-visualização da imagem no formulário de cadastro e edição.
- [x] 4.4 Implementar evento e modal `dialogo_foto_expandida` para exibição da foto em tamanho ampliado ao clicar nas miniaturas/avatars.

## 5. Verificação e Validação Final

- [x] 5.1 Testar as requisições de consulta, criação, edição e exclusão de animais com o backend Xano.
- [x] 5.2 Testar a navegação entre a tela inicial e a Gestão de Animais na Área Administrativa.
- [x] 5.3 Testar a abertura e fechamento do modal de foto expandida em diferentes resoluções.
- [x] 5.4 Executar compilação do projeto e confirmar a ausência de erros de sintaxe nos arquivos da aplicação.