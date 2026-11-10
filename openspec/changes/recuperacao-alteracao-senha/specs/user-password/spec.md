# Spec: Recuperação e Alteração de Senha

## Purpose
Permitir que os usuários do sistema Porto Seguro Pet recuperem o acesso à sua conta ou alterem sua senha de forma simples, segura e visualmente guiada.

## ADDED Requirements

### Requirement: Solicitação de recuperação de senha

O sistema SHALL permitir que o usuário informe seu e-mail cadastrado para solicitar a redefinição de senha.

#### Scenario: Envio de e-mail de recuperação
- **WHEN** o usuário informa um e-mail válido no modal de recuperação e confirma
- **THEN** o sistema envia a solicitação ao Xano e exibe um feedback visual (*toast*) confirmando as instruções.

### Requirement: Interface aprimorada de alteração de senha

O sistema SHALL exibir um formulário interativo de alteração de senha contendo validações visuais e controles de visibilidade.

#### Scenario: Validação e força de senha
- **WHEN** o usuário digita a nova senha
- **THEN** o sistema atualiza em tempo real o indicador visual de força e verifica os critérios mínimos de segurança.

#### Scenario: Visualização do texto da senha
- **WHEN** o usuário clica no ícone de alternância (olho)
- **THEN** o sistema alterna a visibilidade dos caracteres do campo entre texto legível e oculto.

### Requirement: Confirmação e atualização da senha no Xano

O sistema SHALL validar a confirmação dos campos e enviar os dados para atualização no backend.

#### Scenario: Envio de nova senha válida
- **WHEN** os campos "Nova Senha" e "Confirmar Senha" coincidem e atingem os critérios
- **THEN** o sistema executa a requisição ao Xano, confirma o sucesso via *toast* e fecha o modal.