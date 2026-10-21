## 1. Contratos e configuração do Xano

* [ ] 1.1 Confirmar a política de senha vigente para `USUARIO` e os mecanismos de hashing e verificação disponíveis, incluindo `Check Password`
* [ ] 1.2 Definir os contratos de entrada, saída e erros para solicitação de recuperação, confirmação do token e alteração autenticada; registrar as URLs somente após criar as operações no Xano
* [ ] 1.3 Configurar envio de e-mail, remetente e URL de retorno para recuperação de senha
* [ ] 1.4 Implementar a solicitação de recuperação com resposta neutra para e-mail cadastrado ou não cadastrado e limites contra abuso
* [ ] 1.5 Implementar token aleatório, temporário, de uso único, armazenamento seguro, invalidação e rejeição de token expirado ou reutilizado
* [ ] 1.6 Implementar confirmação da recuperação e atualizar a senha pelo mecanismo seguro de hashing do Xano
* [ ] 1.7 Implementar alteração autenticada: identificar a conta pelo contexto da sessão, validar a senha atual com `Check Password` e rejeitar conta indicada pelo cliente
* [ ] 1.8 Definir e testar revogação das sessões existentes após redefinição ou alteração de senha
* [ ] 1.9 Revisar logs e respostas dos fluxos no Xano para garantir que não exponham credenciais, tokens, links ou dados pessoais

## 2. Integração e interface Reflex

* [ ] 2.1 Configurar no ambiente Reflex as URLs reais das operações Xano e documentar os nomes das variáveis em `.env.example`, sem incluir valores secretos
* [ ] 2.2 Adicionar à tela de login o acesso à recuperação e o formulário de solicitação
* [ ] 2.3 Implementar a confirmação de recuperação com token e nova senha, respeitando o contrato confirmado com o Xano
* [ ] 2.4 Adicionar uma opção de alteração de senha acessível aos tipos de usuário autenticados
* [ ] 2.5 Validar campos obrigatórios e confirmação da nova senha no Reflex, mantendo a política definitiva no Xano
* [ ] 2.6 Limpar senha, confirmação e token dos estados de interface após sucesso, cancelamento ou encerramento do fluxo
* [ ] 2.7 Tratar respostas inesperadas e falhas de integração com mensagens neutras e sem registrar dados sensíveis
* [ ] 2.8 Confirmar que a alteração bem-sucedida encerra a sessão local e retorna ao login sem modificar os destinos existentes após autenticação

## 3. Testes e verificação

* [ ] 3.1 Testar solicitação para e-mail cadastrado e não cadastrado e confirmar respostas públicas equivalentes
* [ ] 3.2 Testar envio de e-mail, indisponibilidade do provedor e limites de solicitações sem revelar a existência da conta
* [ ] 3.3 Testar token válido, inválido, expirado, reutilizado e substituído por solicitação posterior
* [ ] 3.4 Testar rejeição de nova senha fora da política e confirmar que a senha existente não é alterada
* [ ] 3.5 Testar alteração autenticada com senha atual correta e incorreta, token ausente/expirado e tentativa de indicar outra conta
* [ ] 3.6 Verificar que senhas e tokens não aparecem em logs, respostas, URLs operacionais ou estado persistente do cliente
* [ ] 3.7 Verificar revogação de sessões conforme decisão do Xano e confirmar encerramento da sessão local no Reflex
* [ ] 3.8 Regressão: testar login válido e inválido com `XANO_LOGIN_URL`/`XANO_ME_URL` e direcionamentos para `/administrativo` e `/tutor`
* [ ] 3.9 Executar `python -m py_compile ProjetoONG/ProjetoONG.py` e validar a change com `openspec validate --changes recuperacao-alteracao-senha`