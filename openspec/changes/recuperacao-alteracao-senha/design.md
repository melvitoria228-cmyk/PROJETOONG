# Design: Recuperação e Alteração de Senha

## Context & Vision
O fluxo de alteração e recuperação de senha é fundamental para garantir a segurança da conta e a autonomia do usuário (tanto Tutores quanto Administradores). A interface deve ser moderna, intuitiva e guiar o usuário visualmente para evitar erros de digitação e garantir senhas fortes.

## User Interface (UI) & User Experience (UX)
- **Modal Responsivo e Focado:** Exibido centralizado via `rx.dialog` com ícone temático de segurança (`lock`).
- **Indicador Dinâmico de Força de Senha:** Barra de progresso (`rx.progress`) que se altera dinamicamente entre vermelho (fraca), laranja (média) e verde (forte) de acordo com o comprimento e diversidade dos caracteres.
- **Controle de Visibilidade:** Botão com ícone de olho (`rx.icon(tag="eye")` / `rx.icon(tag="eye_off")`) para alternar a visibilidade da senha em tempo real.
- **Validação de Confirmação:** Feedback visual instantâneo sinalizando se os campos "Nova Senha" e "Confirmar Senha" coincidem.
- **Estado dos Botões:** Desabilitação automática do botão de envio enquanto a senha for fraca ou os campos não coincidirem, prevenindo requisições inválidas ao backend.

## Technical Architecture & Data Flow
- **State Management (Reflex):** `ChangePasswordState` centraliza as variáveis `show_password`, `new_password`, `confirm_password` e as propriedades calculadas (`password_strength`, `passwords_match`).
- **Integração Backend (Xano):** 
  - Envio dos dados via requisição HTTP (`POST`) para os endpoints de redefinição/alteração do Xano.
  - Exibição de mensagens de sucesso ou erro usando `rx.toast`.