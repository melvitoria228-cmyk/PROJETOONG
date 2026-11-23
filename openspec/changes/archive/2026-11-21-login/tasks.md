## 1. Preparação

- [x] 1.1 Confirmar a estrutura inicial do frontend Reflex e verificar que o projeto continua executando com `reflex run`.
- [x] 1.2 Preparar a estrutura da tela de login (`pagina_login`) na rota `/` em `ProjetoONG/ProjetoONG.py` e verificar que pode ser acessada sem conflitar com as demais rotas.

## 2. Interface de Login e Carrossel Visual

- [x] 2.1 Criar a tela única de login enxuta e acolhedora para `TUTOR/ADOTANTE` e `ADMINISTRADOR`, garantindo que os dois perfis utilizem a mesma interface inicial.
- [x] 2.2 Implementar o carrossel de fotos de animais na lateral esquerda com transição automática em segundo plano (`iniciar_carrossel_automatico` no `on_load`).
- [x] 2.3 Adicionar os campos de e-mail e senha com controle de alternância de visibilidade da senha.
- [x] 2.4 Adicionar o botão de acesso com indicador de carregamento durante a requisição de autenticação.
- [x] 2.5 Implementar a validação dos campos obrigatórios antes do envio à API, exibindo alerta via `rx.toast` caso e-mail ou senha estejam vazios.
- [x] 2.6 Revisar a apresentação visual da tela de login, mantendo o formulário direto (sem links ou botões de alteração de senha) e alinhado à identidade visual do projeto.

## 3. Integração com o Xano

- [x] 3.1 Configurar a leitura da variável `XANO_LOGIN_URL` via `.env` e verificar que a aplicação identifica quando a URL está configurada.
- [x] 3.2 Integrar o envio assíncrono (`httpx`) de e-mail e senha ao endpoint de login do Xano e verificar o recebimento do token JWT.
- [x] 3.3 Tratar credenciais inválidas e falhas de conexão apresentando mensagens claras de erro via `rx.toast`.
- [x] 3.4 Configurar a leitura da variável `XANO_ME_URL` para o endpoint `/auth/me`.
- [x] 3.5 Utilizar o token JWT retornado pelo login para consultar `/auth/me` e capturar o `tipo_usuario` e os dados cadastrais vinculados à sessão.
- [x] 3.6 Identificar o perfil retornado pelo Xano e verificar o reconhecimento de `TUTOR/ADOTANTE` e `ADMINISTRADOR`.
- [x] 3.7 Tratar respostas inesperadas da consulta de usuário e garantir que o sistema não considere o login confirmado sem identificação válida.

## 4. Direcionamento e Encerramento de Sessão

- [x] 4.1 Direcionar o `ADMINISTRADOR` para `/administrativo` após autenticação válida e verificar o redirecionamento.
- [x] 4.2 Direcionar o `TUTOR/ADOTANTE` para `/tutor` após autenticação válida e verificar o redirecionamento.
- [x] 4.3 Tratar tipos de usuário desconhecidos e confirmar que não recebem acesso às rotas restritas.
- [x] 4.4 Implementar o encerramento seguro de sessão (`LoginState.sair`), limpando o token JWT e os dados da sessão e redirecionando para `/`.

## 5. Verificação Final

- [x] 5.1 Testar o login com campos vazios e verificar que a tentativa é impedida.
- [x] 5.2 Testar o login com credenciais inválidas e verificar que o acesso é impedido.
- [x] 5.3 Testar o login com credenciais válidas e verificar que o token é utilizado para consultar o usuário autenticado e carregar o contexto da sessão.
- [x] 5.4 Testar a identificação de `TUTOR/ADOTANTE` e `ADMINISTRADOR` com contas correspondentes e o fluxo de logout.
- [x] 5.5 Executar `python -m py_compile ProjetoONG/ProjetoONG.py` e verificar que o arquivo não apresenta erros de sintaxe.
- [x] 5.6 Executar `openspec validate --changes login` e verificar que a change é validada sem falhas.