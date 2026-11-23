# Design: Recuperação e Alteração de Senha

## Context

O módulo de **Recuperação e Alteração de Senha** atende tanto Administradores quanto Tutores/Adotantes do **Porto Seguro Pet**, oferecendo um fluxo autônomo e seguro para recuperar o acesso a partir da tela de Login (rota `/`) ou atualizar a senha da conta.

A implementação utiliza componentes nativos do **Reflex** (`rx.dialog`, `rx.progress`, `rx.icon` e `rx.toast`) integrados de forma assíncrona (`httpx.AsyncClient`) aos endpoints de recuperação e redefinição de senha do backend **Xano** configurados via `.env`.

## Goals / Non-Goals

### Goals

- Disponibilizar um modal de **solicitação de recuperação de senha** na tela de Login (`/`) para envio de e-mail cadastrado e disparo de código/token de redefinição via Xano.
- Disponibilizar um modal focado de **redefinição e alteração de senha** (`rx.dialog`) com ícone temático de segurança (`lock`) e paleta institucional do Porto Seguro Pet.
- Fornecer **indicador dinâmico de força da senha** (`rx.progress`) alternando visualmente entre fraca (vermelho), média (laranja) e forte (verde/oliva) conforme comprimento e diversidade de caracteres.
- Permitir alternar a visibilidade dos campos de senha (`eye` / `eye_off`) e validar em tempo real a coincidência entre **Nova Senha** e **Confirmar Senha**, mantendo o botão de envio desabilitado enquanto os critérios mínimos não forem atendidos.
- Integrar todas as requisições (`POST`) ao **Xano** via `httpx.AsyncClient` com tratamento de erros, feedback via `rx.toast` e limpeza automática dos campos sensíveis ao fechar ou concluir o fluxo.

### Non-Goals

- Armazenar senhas em texto plano ou persistir valores de senha no armazenamento local do navegador.
- Implementar múltiplos fatores de autenticação via SMS ou aplicativos autenticadores nesta etapa.
- Alterar o esquema de tabelas já existente no Xano além dos endpoints padrão de autenticação e recuperação de senha.

## Decisions

### 1. Fluxo em Duas Etapas (Solicitação e Redefinição/Alteração)

- **Etapa 1 — Solicitação de Recuperação (Rota `/`):** acionada pelo link *"Esqueci minha senha"* na tela de Login, abre um `rx.dialog` onde o usuário informa seu e-mail cadastrado. O envio dispara uma requisição `POST` para o endpoint de solicitação de recuperação do Xano.
- **Etapa 2 — Redefinição / Alteração de Senha:** abre o modal dedicado (`rx.dialog`) com ícone `lock`, solicitando o código/token de recuperação (ou senha atual, quando autenticado), a **Nova Senha** e a **Confirmação de Senha**.

### 2. Gerenciamento de Estado Reativo (`ChangePasswordState` / `LoginState`)

- Centraliza os estados de controle (`show_password`, `show_confirm_password`, `recovery_email`, `reset_token`, `new_password`, `confirm_password`, `is_submitting`) e as propriedades computadas (`@rx.var`):
  - `password_strength`: avalia comprimento mínimo, letras maiúsculas/minúsculas, números e caracteres especiais, retornando pontuação e cor semântica para o `rx.progress`.
  - `passwords_match`: compara em tempo real `new_password` e `confirm_password`, exibindo feedback visual imediato.
  - `can_submit`: habilita o botão de confirmação apenas quando a força mínima é atingida, as senhas coincidem e não há requisição em andamento.
- Ao fechar qualquer modal (`on_open_change`), os campos sensíveis de senha e token são limpos automaticamente da memória do estado.

### 3. Integração Autenticada e Segura com o Xano

- As requisições assíncronas (`POST`) utilizam `httpx.AsyncClient` apontando para as URLs configuradas no `.env` (`XANO_FORGOT_PASSWORD_URL` / `XANO_RESET_PASSWORD_URL`), incluindo o cabeçalho `Authorization: Bearer <token>` (`LoginState.token`) quando a alteração ocorre em sessão autenticada.
- Respostas de sucesso e falhas de validação ou expiração de token são comunicadas imediatamente ao usuário por meio de `rx.toast`.

### 4. Identidade Visual Institucional

- Os modais seguem a identidade visual do **Porto Seguro Pet** (superfícies Bege Claro `#F8F3EC` e Areia `#EFE6DA`, textos em Café Escuro `#2D1F18` e ações principais em Terracota `#A96348` / `#A65F43`).

## Risks / Trade-offs

- **Expiração ou digitação incorreta do token de recuperação** → Tratada com captura de resposta HTTP do Xano e exibição de mensagem orientativa via `rx.toast`, permitindo solicitar um novo envio sem recarregar a página.
- **Persistência residual de dados sensíveis no estado Reflex** → Mitigada resetando explicitamente `new_password`, `confirm_password` e `reset_token` tanto após o sucesso da operação quanto no fechamento do modal.

## Migration Plan

1. Configurar as URLs dos endpoints de recuperação e redefinição de senha do Xano no `.env`.
2. Implementar os estados reativos, getters de força/coincidência de senha e handlers assíncronos em `ProjetoONG/login_state.py` (`ChangePasswordState` / `LoginState`).
3. Construir os modais de solicitação de recuperação e alteração/redefinição de senha e integrá-los à tela de Login (`ProjetoONG/login.py` / `ProjetoONG/ProjetoONG.py`).
4. Validar o fluxo completo de envio de e-mail, cálculo dinâmico de força da senha, alternância de visibilidade, bloqueio de botão inválido e confirmação junto ao Xano.