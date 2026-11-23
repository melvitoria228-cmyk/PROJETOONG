# Spec: Recuperação e Alteração de Senha

## Purpose

Permitir que os usuários do **Porto Seguro Pet** (administradores e tutores/adotantes) solicitem a recuperação de acesso por e-mail/token e redefinam ou alterem sua senha de forma segura, autônoma e visualmente guiada junto ao backend Xano.

## ADDED Requirements

### Requirement: Solicitação de Recuperação de Senha

O sistema SHALL permitir que o usuário informe seu e-mail cadastrado no modal de recuperação (acionado a partir da tela de Login na rota `/`) para solicitar o envio de código/token de redefinição via Xano.

#### Scenario: Envio de e-mail de recuperação com sucesso
- **WHEN** o usuário informa um e-mail válido no modal de recuperação e confirma o envio
- **THEN** o sistema SHALL enviar a solicitação (`POST`) ao endpoint de recuperação do Xano
- **AND** SHALL exibir um feedback visual (*toast*) confirmando o envio das instruções de redefinição.

#### Scenario: Falha ou e-mail inválido na solicitação
- **WHEN** o usuário informa um e-mail inválido ou ocorre falha na comunicação com o Xano
- **THEN** o sistema SHALL impedir o envio inválido ou exibir mensagem orientativa via *toast* sem fechar abruptamente o modal.

### Requirement: Interface Aprimorada de Redefinição e Alteração de Senha

O sistema SHALL exibir um modal dedicado (`rx.dialog`) de redefinição/alteração de senha contendo indicador dinâmico de força, alternância de visibilidade e validação em tempo real de coincidência entre os campos.

#### Scenario: Validação dinâmica e indicador de força da senha
- **WHEN** o usuário digita a nova senha no campo correspondente
- **THEN** o sistema SHALL atualizar em tempo real a barra de progresso (`rx.progress`) refletindo a força da senha (fraca, média ou forte) e verificar os critérios mínimos de segurança.

#### Scenario: Alternância de visibilidade da senha
- **WHEN** o usuário aciona o ícone de alternância (`eye` / `eye_off`) de um campo de senha
- **THEN** o sistema SHALL alternar imediatamente a exibição dos caracteres entre texto legível e oculto.

#### Scenario: Bloqueio de envio com senha fraca ou divergente
- **WHEN** a nova senha não atinge a força mínima exigida ou os campos "Nova Senha" e "Confirmar Senha" não coincidem
- **THEN** o sistema SHALL sinalizar visualmente a divergência e manter o botão de confirmação desabilitado.

### Requirement: Confirmação, Atualização no Xano e Limpeza de Dados Sensíveis

O sistema SHALL enviar a nova senha válida ao backend Xano, notificar o resultado via *toast* e limpar os campos sensíveis da memória do estado.

#### Scenario: Envio de nova senha válida com sucesso
- **WHEN** os campos "Nova Senha" e "Confirmar Senha" coincidem, atingem os critérios mínimos e o usuário confirma o envio
- **THEN** o sistema SHALL executar a requisição autenticada (`POST`) ao endpoint de redefinição/alteração de senha do Xano
- **AND** SHALL confirmar o sucesso via *toast*, limpar os campos sensíveis de senha/token e fechar o modal.

#### Scenario: Erro ou token expirado na atualização da senha
- **WHEN** o Xano rejeita a atualização (como token expirado ou erro de rede)
- **THEN** o sistema SHALL manter o modal aberto e exibir uma mensagem de erro orientativa via *toast*.