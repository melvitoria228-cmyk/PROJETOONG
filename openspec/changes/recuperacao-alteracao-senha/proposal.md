# Proposal: Recuperação e Alteração de Senha

## Why
O sistema precisa oferecer um mecanismo seguro e intuitivo para que os usuários possam recuperar o acesso à conta e alterar sua senha, garantindo a proteção dos dados e uma experiência de usuário (UX) clara e acolhedora.

## What Changes
- Implementar o fluxo de solicitação de redefinição de senha com envio de e-mail/token.
- Criar/Aprimorar a interface visual do modal de alteração de senha com:
  - Indicador dinâmico de força da senha.
  - Alternância para mostrar/ocultar senha (ícone de olho).
  - Validação visual em tempo real para coincidência de senhas.
- Integrar com os endpoints de redefinição/alteração de senha do Xano.

## Capabilities
### New Capabilities
- `password-recovery`: capacidade de recuperar e alterar senha de acesso via e-mail e modais dedicados.

### Modified Capabilities
Nenhuma.