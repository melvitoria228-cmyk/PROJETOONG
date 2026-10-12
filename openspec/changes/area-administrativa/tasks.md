## 1. Preparação

* [x] 1.1 Confirmar a estrutura inicial do frontend Reflex e verificar que o projeto continua executando com `reflex run`
* [x] 1.2 Preparar a estrutura da tela de login no frontend e verificar que a nova tela pode ser acessada sem alterar as demais partes do projeto

## 2. Interface de Login

* [x] 2.1 Criar a tela única de login para TUTOR/ADOTANTE e ADMINISTRADOR e verificar que ambos utilizam a mesma interface
* [x] 2.2 Adicionar os campos de e-mail e senha e verificar que ambos aparecem corretamente na tela
* [x] 2.3 Adicionar o botão de acesso e verificar que ele pode ser acionado pelo usuário
* [x] 2.4 Implementar a validação dos campos obrigatórios e verificar que a tentativa sem e-mail ou senha é impedida e apresenta uma mensagem ao usuário
* [x] 2.5 Revisar a apresentação visual da tela de login e verificar que a interface está organizada, simples e adequada à identidade visual do projeto

## 3. Integração com o Xano

* [x] 3.1 Configurar a leitura da variável `XANO_LOGIN_URL` e verificar que a aplicação identifica quando a URL está configurada
* [x] 3.2 Integrar o envio de e-mail e senha ao endpoint de login do Xano e verificar que a autenticação retorna uma resposta válida para credenciais corretas
* [x] 3.3 Tratar credenciais inválidas e falhas de conexão e verificar que o frontend apresenta mensagens adequadas
* [x] 3.4 Armazenar o token de autenticação após o login e verificar que ele pode ser utilizado na consulta autenticada
* [x] 3.5 Consultar o endpoint `/auth/me` usando o token e verificar o recebimento de `id`, `email` e `tipo_usuario`
* [x] 3.6 Tratar respostas inesperadas do login e da consulta de usuário e verificar que o acesso não é concedido quando a autenticação não pode ser confirmada

## 4. Identificação e Direcionamento

* [x] 4.1 Identificar o tipo de usuário retornado pelo Xano e verificar o reconhecimento de TUTOR/ADOTANTE e ADMINISTRADOR
* [x] 4.2 Direcionar o administrador para `/administrativo` e verificar o comportamento após um login válido
* [x] 4.3 Preparar a rota inicial de TUTOR/ADOTANTE conforme o escopo da change e verificar o direcionamento após um login válido
* [ ] 4.4 Verificar o comportamento para tipos de usuário desconhecidos e confirmar que não recebem acesso a uma área restrita

## 5. Controle de Acesso

* [ ] 5.1 Verificar o acesso direto à rota `/administrativo` sem autenticação e implementar a proteção necessária
* [x] 5.2 Verificar que um usuário autenticado como TUTOR/ADOTANTE não recebe acesso à área administrativa
* [ ] 5.3 Verificar que o estado de autenticação é tratado corretamente ao sair da sessão ou quando o token deixa de ser válido

## 6. Verificação Final

* [x] 6.1 Testar o login com campos vazios e verificar que a tentativa é impedida
* [x] 6.2 Testar o login com credenciais inválidas e verificar que o acesso é impedido
* [x] 6.3 Testar o login com credenciais válidas e verificar que o token é utilizado para identificar o usuário
* [x] 6.4 Testar o fluxo de administrador e verificar a identificação e o direcionamento corretos
* [x] 6.5 Testar o fluxo de TUTOR/ADOTANTE e verificar a identificação e o direcionamento previstos
* [x] 6.6 Executar `python -m py_compile ProjetoONG/ProjetoONG.py` e verificar que o arquivo não apresenta erros de sintaxe

