# Proposal: Recuperação e Alteração de Senha

## Why

Os usuários do **Porto Seguro Pet** (administradores e tutores/adotantes) precisam de um fluxo seguro, autônomo e intuitivo para recuperar o acesso à conta em caso de esquecimento e redefinir ou alterar sua senha sem depender de intervenção manual da equipe técnica.

Integrar esse fluxo diretamente à tela de autenticação (rota `/`) e aos endpoints do backend **Xano**, com feedbacks visuais claros de força e coincidência de senha, aumenta a proteção das contas e torna a experiência de acesso mais acolhedora.

## What Changes

- Implementar o modal e o fluxo de **solicitação de recuperação de senha** acionado a partir da tela de Login (rota `/`), permitindo informar o e-mail cadastrado para envio do código/token de redefinição via endpoint do **Xano**.
- Implementar/aprimorar a interface visual do **modal de redefinição e alteração de senha** seguindo a paleta institucional do Porto Seguro Pet, contendo:
  - Indicador dinâmico de força da senha em tempo real (com critérios claros de segurança).
  - Alternância individual para mostrar/ocultar cada campo de senha (ícone de olho).
  - Validação visual em tempo real para coincidência entre a nova senha e a confirmação de senha, bloqueando o envio enquanto os critérios não forem atendidos.
- Integrar de forma assíncrona (`httpx`) as etapas de solicitação de recuperação e confirmação de nova senha aos endpoints dedicados do **Xano** configurados no `.env`, com notificações via `rx.toast` e limpeza automática dos campos sensíveis.

## Capabilities

### New Capabilities

- `password-recovery`: capacidade de solicitar recuperação de acesso por e-mail/token e redefinir ou alterar a senha da conta por meio de modais dedicados com validação visual em tempo real e integração com o Xano.

### Modified Capabilities

Nenhuma.

## Impact

- **Frontend Reflex (`ProjetoONG/login_state.py` e `ProjetoONG/login.py` / `ProjetoONG/ProjetoONG.py`):** adição dos estados reativos, getters de força/validação de senha, handlers assíncronos e modais de solicitação de recuperação e redefinição de senha na rota `/`.
- **Backend Xano:** integração via `httpx` com os endpoints de recuperação e redefinição/alteração de senha configurados via variáveis de ambiente no `.env`.
- **Segurança e UX:** limpeza imediata dos estados de senha após conclusão ou fechamento dos modais e orientação clara ao usuário via `rx.toast`.