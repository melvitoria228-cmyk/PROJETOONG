# Tasks: Recuperação e Alteração de Senha

## 1. Interface e Componentes Visuais (Reflex)

- [x] 1.1 Atualizar o `ChangePasswordState` no Reflex com o cálculo dinâmico de força da senha e verificação de coincidência entre campos.
- [x] 1.2 Implementar a alternância de visibilidade do texto da senha (mostrar/ocultar via ícone de olho).
- [x] 1.3 Adicionar a barra de progresso e o indicador de cor/status da força da senha no modal.
- [x] 1.4 Adicionar a mensagem e validação visual em tempo real para confirmação das senhas.
- [x] 1.5 Aplicar os estados de carregamento (`is_loading`) e desabilitação condicional no botão de envio.

## 2. Integração com o Xano

- [x] 2.1 Configurar o endpoint no Xano para alteração/redefinição de senha.
- [x] 2.2 Conectar a ação do formulário do Reflex à requisição da API Xano.
- [x] 2.3 Exibir feedbacks visuais via `rx.toast` para casos de sucesso e tratamento de erros.

## 3. Validação e Qualidade

- [x] 3.1 Testar a validação em tempo real com senhas fracas, médias e fortes.
- [x] 3.2 Validar se a tentativa de envio é bloqueada quando as senhas não coincidem.
- [x] 3.3 Executar `python -m py_compile` para garantir que não há erros de sintaxe no Reflex.
- [x] 3.4 Executar `openspec validate --changes recuperacao-alteracao-senha` e confirmar a aprovação da change.