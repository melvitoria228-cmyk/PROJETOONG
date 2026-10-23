## 1. Preparação e validação

- [x] 1.1 Conferir os requisitos e o design da mudança.
- [x] 1.2 Executar `openspec validate --changes area-tutor-adotante` e confirmar que não há falhas.
- [x] 1.3 Conferir a implementação atual do login e o registro das páginas em `ProjetoONG/ProjetoONG.py`.

## 2. Implementação da página inicial

- [x] 2.1 Criar a função da página inicial do Tutor/Adotante em `ProjetoONG/ProjetoONG.py`.
- [x] 2.2 Criar um cabeçalho superior com a marca Porto Seguro Pet, botão de logout interativo e identificação da área.
- [x] 2.3 Criar uma área de boas-vindas com mensagem acolhedora.
- [x] 2.4 Organizar o layout em duas colunas: bloco de resumo de dados e cartões de serviços à esquerda, e o feed de solicitações de adoção à direita.
- [x] 2.5 Criar os três cartões/blocos de atalhos para serviços: "Meus dados", "Acompanhamento" e "Orientações".
- [x] 2.6 Aplicar a paleta grafite `#2D3142` / `#3E4149`, creme `#FFF7ED` / `#F4E7D5` e terracota `#D78A45` / `#684638`.
- [x] 2.7 Registrar a página na rota `/tutor`.
- [x] 2.8 Conferir a apresentação inicial dos cartões e do perfil do tutor.

## 3. Autenticação e redirecionamento

- [x] 3.1 Verificar o redirecionamento de usuários autenticados do tipo `administrador` para `/administrativo`.
- [x] 3.2 Verificar o redirecionamento de usuários autenticados do tipo `tutor/adotante` para `/tutor`.
- [x] 3.3 Verificar que um tipo de usuário desconhecido não recebe redirecionamento para uma área restrita e exibe mensagem de alerta.
- [x] 3.4 Executar a aplicação e testar a abertura da rota `/tutor` no navegador.

## 4. Consulta dos processos de adoção

- [x] 4.1 Configurar a consulta dos processos de adoção por meio do endpoint GET do Xano.
- [x] 4.2 Utilizar o token de autenticação na consulta.
- [x] 4.3 Testar a consulta e confirmar o recebimento de dados reais do backend.
- [x] 4.4 Configurar o Add-on no Xano para retornar o objeto do animal (`_animal`) associado a cada processo de adoção.
- [x] 4.5 Exibir o nome real do animal no cabeçalho do cartão de solicitação em vez de apenas o ID numérico.
- [x] 4.6 Implementar indicador visual de progresso por etapas (1. Análise, 2. Aprovação, 3. Concluído) e caixas explicativas para o status da solicitação.
- [x] 4.7 Testar a apresentação dos dados com processos reais, com falhas de conexão e com a ausência de resultados (estado vazio).

## 5. Navegação pelos cartões e subpáginas

- [x] 5.1 Tornar o feed de "Minhas adoções" visível na tela principal do tutor e acessível na rota `/minhas-adocoes`.
- [x] 5.2 Conectar o cartão "Acompanhamento" à página `/acompanhamento`.
- [x] 5.3 Conectar o cartão "Meus dados" à página `/meus-dados`.
- [x] 5.4 Conectar o cartão "Orientações" à página `/orientacoes`.
- [x] 5.5 Testar a navegação e o retorno de todas as páginas para o painel `/tutor` por meio de botões de voltar com transição suave.

## 6. Acompanhamento pós-adoção

- [x] 6.1 Conferir a estrutura da tabela de acompanhamento pós-adoção no Xano.
- [x] 6.2 Configurar o endpoint `XANO_ACOMPANHAMENTO_LIST_URL` para consultar os registros de acompanhamento.
- [x] 6.3 Criar a página `/acompanhamento` com cartão explicativo ("Como funciona") e feed de relatórios.
- [x] 6.4 Exibir os registros de visitas e observações vinculados ao tutor autenticado.
- [x] 6.5 Testar a consulta de acompanhamentos, o tratamento de ausência de registros e mensagens de erro.

## 7. Meus dados e Orientações

- [x] 7.1 Capturar os dados do tutor cadastrado (`id`, `nome`, `cpf`, `telefone`, `tipo_residencia`, `endereco`) no login a partir da resposta da API Xano.
- [x] 7.2 Criar a página `/meus-dados` com formulário de edição para atualização do perfil.
- [x] 7.3 Conectar o botão "Salvar Alterações" da página `/meus-dados` ao endpoint `PATCH /tutor_adotante` do Xano com alertas via `rx.toast`.
- [x] 7.4 Definir o conteúdo informativo educativo para o guia de guarda responsável.
- [x] 7.5 Criar a página `/orientacoes` detalhando dicas de adaptação, saúde, vacinação e segurança.
- [x] 7.6 Testar a edição de dados e a navegação entre as telas.

## 8. Validação final

- [x] 8.1 Testar o fluxo de login, o logout e os redirecionamentos por perfil.
- [x] 8.2 Testar a navegação pelos 3 cartões de serviços e suas respectivas subpáginas.
- [x] 8.3 Conferir a apresentação clara dos dados de adoção, do nome do pet e do indicador de progresso por etapas.
- [x] 8.4 Conferir a identidade visual institucional (grafite, creme e terracota) e a consistência em todas as páginas do tutor.
- [x] 8.5 Verificar a persistência das alterações de perfil no backend Xano.
- [x] 8.6 Executar `openspec validate --changes area-tutor-adotante` e confirmar que a documentação continua válida.