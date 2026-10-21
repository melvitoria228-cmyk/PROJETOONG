# Proposal: Recuperação e Alteração de Senha

## Problema

O Porto Seguro Pet oferece login por e-mail e senha, mas ainda não possui um fluxo de recuperação para quem perdeu acesso nem uma forma de trocar a senha a partir de uma sessão autenticada. A mudança não pode permitir redefinição baseada apenas no conhecimento do e-mail.

## Objetivo

Permitir que uma pessoa prove controle do e-mail cadastrado antes de redefinir a senha e que um usuário autenticado altere a própria senha após validar a senha atual.

## Escopo

* Solicitar recuperação informando o e-mail cadastrado, sem revelar se a conta existe.
* Enviar uma verificação por e-mail e permitir a redefinição somente após validar um token temporário, de uso único e não expirado.
* Permitir a alteração da senha para usuário autenticado, validando a senha atual no Xano antes de salvar a nova.
* Integrar os fluxos à interface Reflex e à autenticação existente do Xano, preservando o login e o direcionamento por tipo de usuário.
* Definir e testar tratamento seguro de falhas e de dados sensíveis.

## Fora do escopo

* Alterar o fluxo de login, o formato do token de autenticação ou os redirecionamentos existentes.
* Criar cadastro de usuários ou alterar e-mail, tipo de usuário ou outras informações de perfil.
* Definir rotas Xano como se já existissem. Os contratos e URLs serão confirmados e implementados no Xano antes da integração Reflex.
* Exibir, armazenar ou transmitir a senha em texto simples em banco de dados, logs ou respostas de API.

## Dependências

* Configurar no Xano as operações necessárias para iniciar a recuperação, validar o token e redefinir a senha, e alterar a senha autenticada.
* Confirmar que a tabela `USUARIO` e o mecanismo de autenticação do Xano permitem armazenar senha com hash e validar a senha atual por `Check Password`.
* Configurar um provedor de envio de e-mail, remetente e URL de retorno para a mensagem de recuperação.
* Definir limites de tentativas, validade do token, política de senha e comportamento de revogação de sessões no Xano.
* Disponibilizar ao Reflex as URLs reais dessas operações somente depois de criadas. Nomes de variáveis de ambiente serão definidos na implementação, sem pressupor rotas existentes.

## Resultado esperado

O usuário consegue recuperar a senha somente após comprovar acesso ao e-mail cadastrado, ou alterar a própria senha depois de informar corretamente a senha atual. O login atual continua funcionando e nenhum segredo aparece em logs ou respostas.