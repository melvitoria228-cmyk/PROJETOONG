## 1. Preparação

* [x] 1.1 Confirmar a estrutura inicial do frontend Reflex e verificar que o projeto continua executando com `reflex run`
* [x] 1.2 Preparar a estrutura da tela de login no frontend e verificar que a nova tela pode ser acessada sem alterar as demais partes do projeto

## 2. Interface de Login

* [x] 2.1 Criar a tela única de login para TUTOR/ADOTANTE e ADMINISTRADOR e verificar que os dois tipos de usuário podem utilizar a mesma interface
* [x] 2.2 Adicionar os campos de e-mail e senha e verificar que ambos aparecem corretamente na tela
* [x] 2.3 Adicionar o botão de acesso e verificar que ele pode ser acionado pelo usuário
* [x] 2.4 Implementar a validação dos campos obrigatórios e verificar que a tentativa sem e-mail ou senha é impedida e apresenta uma mensagem ao usuário
* [x] 2.5 Revisar a apresentação visual da tela de login e verificar que a interface está organizada, simples e adequada à identidade visual do projeto

## 3. Integração com o Xano

* [x] 3.1 Configurar a leitura da variável `XANO_LOGIN_URL` e verificar que a aplicação identifica quando a URL está configurada
* [x] 3.2 Integrar o envio de e-mail e senha ao endpoint de login do Xano e verificar que a autenticação retorna uma resposta válida para credenciais corretas
* [x] 3.3 Tratar credenciais inválidas e falhas de conexão e verificar que o frontend apresenta mensagens adequadas
* [x] 3.4 Configurar a URL do endpoint `/auth/me` e verificar que a variável `XANO_ME_URL` é carregada corretamente
* [x] 3.5 Utilizar o token retornado pelo login para consultar `/auth/me` e verificar o recebimento dos dados do usuário autenticado
* [x] 3.6 Identificar o tipo de usuário retornado pelo Xano e verificar o reconhecimento de TUTOR/ADOTANTE e ADMINISTRADOR
* [ ] 3.7 Tratar respostas inesperadas da consulta de usuário e verificar que o sistema não considera o login confirmado quando não consegue identificar o usuário

## 4. Direcionamento após o Login

* [x] 4.1 Direcionar o ADMINISTRADOR para `/administrativo` após autenticação válida e verificar o redirecionamento.
* [x] 4.2 Direcionar o TUTOR/ADOTANTE para `/tutor` após autenticação válida, deixando a implementação da tela para uma mudança específica.
* [ ] 4.3 Tratar tipos de usuário desconhecidos e confirmar que não recebem acesso a áreas restritas.
* [x] 4.4 Verificar que o direcionamento só ocorre após a autenticação e a identificação do tipo de usuário serem confirmadas.


## 5. Verificação Final

* [x] 5.1 Testar o login com campos vazios e verificar que a tentativa é impedida
* [x] 5.2 Testar o login com credenciais inválidas e verificar que o acesso é impedido
* [x] 5.3 Testar o login com credenciais válidas e verificar que o token é utilizado para consultar o usuário autenticado
* [x] 5.4 Testar a identificação de TUTOR/ADOTANTE e ADMINISTRADOR com contas correspondentes
* [x] 5.5 Executar `python -m py_compile ProjetoONG/ProjetoONG.py` e verificar que o arquivo não apresenta erros de sintaxe
* [x] 5.6 Executar `openspec validate --changes login` e verificar que a change é validada sem falhas
