# Tasks: Recuperação e Alteração de Senha

## 1. Estado e Regras de Validação (`ProjetoONG/login_state.py`)

- [x] 1.1 Atualizar `ChangePasswordState` / `LoginState` em `ProjetoONG/login_state.py` com os estados de controle (`recovery_email`, `reset_token`, `new_password`, `confirm_password`, `show_password`, `is_loading`) e os getters reativos (`@rx.var`) de força da senha (`password_strength`) e coincidência (`passwords_match`).
- [x] 1.2 Implementar a lógica de limpeza automática dos campos sensíveis de senha e token ao concluir a operação ou fechar os modais (`on_open_change`).

## 2. Interface e Modais (`ProjetoONG/login.py` / `ProjetoONG/ProjetoONG.py`)

- [x] 2.1 Implementar/aprimorar o modal de solicitação de recuperação de senha (`rx.dialog`) acionado a partir da tela de Login (rota `/`) seguindo a paleta institucional do Porto Seguro Pet.
- [x] 2.2 Implementar/aprimorar o modal de redefinição e alteração de senha (`rx.dialog`) com ícone temático de segurança (`lock`) e alternância individual de visibilidade via ícone de olho (`eye` / `eye_off`).
- [x] 2.3 Adicionar a barra de progresso dinâmica (`rx.progress`) e o indicador de cor/status da força da senha (fraca, média e forte).
- [x] 2.4 Adicionar a validação visual em tempo real para coincidência entre "Nova Senha" e "Confirmar Senha" e aplicar a desabilitação condicional do botão de envio durante carregamento ou critérios não atendidos.

## 3. Integração Autenticada com o Xano

- [x] 3.1 Configurar as URLs dos endpoints de recuperação e redefinição/alteração de senha do Xano via `.env`.
- [x] 3.2 Conectar os handlers assíncronos (`httpx.AsyncClient`) do Reflex aos endpoints de solicitação de e-mail/token e atualização de senha no Xano (enviando `Authorization: Bearer <token>` quando em sessão autenticada).
- [x] 3.3 Exibir feedbacks visuais via `rx.toast` para confirmação de envio de e-mail, sucesso na alteração e tratamento de erros ou token expirado.

## 4. Validação e Qualidade

- [x] 4.1 Testar a validação em tempo real com senhas fracas, médias e fortes, bem como o bloqueio de envio quando as senhas não coincidem.
- [x] 4.2 Executar `python -m py_compile` para garantir a ausência de erros de sintaxe nos módulos Reflex.
- [x] 4.3 Executar `openspec validate --changes recuperacao-alteracao-senha` e confirmar a aprovação da change.