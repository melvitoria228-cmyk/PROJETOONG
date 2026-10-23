# Spec: Login

## Purpose

Permitir que usuários autorizados acessem o sistema Porto Seguro Pet de acordo com seu tipo de usuário, garantindo um acesso simples, seguro e acolhedor às áreas correspondentes.

## ADDED Requirements

### Requirement: Acesso com credenciais válidas e direcionamento por perfil

O sistema SHALL permitir o acesso quando o usuário informar um e-mail e uma senha correspondentes a uma conta válida no Xano, redirecionando o usuário para a área correspondente ao seu perfil.

#### Scenario: Login com credenciais válidas do tipo ADMINISTRADOR
- **WHEN** o usuário informar e-mail e senha válidos de uma conta do tipo `ADMINISTRADOR`
- **THEN** o sistema autentica o usuário via Xano, armazena o token JWT de sessão e redireciona automaticamente para a rota `/administrativo`

#### Scenario: Login com credenciais válidas do tipo TUTOR/ADOTANTE
- **WHEN** o usuário informar e-mail e senha válidos de uma conta do tipo `TUTOR/ADOTANTE`
- **THEN** o sistema autentica o usuário via Xano, armazena o token JWT de sessão e redireciona automaticamente para a rota `/tutor`

### Requirement: Tratamento de credenciais inválidas e falhas

O sistema SHALL impedir o acesso quando o e-mail ou a senha informados não corresponderem a uma conta válida ou houver falha de conexão.

#### Scenario: Login com credenciais inválidas
- **WHEN** o usuário informar credenciais inválidas
- **THEN** o sistema impede o acesso e exibe uma mensagem clara de erro para o usuário

### Requirement: Campos obrigatórios do login

O sistema SHALL exigir o preenchimento do e-mail e da senha para realizar uma tentativa de login.

#### Scenario: Campos não preenchidos
- **WHEN** o usuário tentar realizar login sem informar e-mail ou senha
- **THEN** o sistema impede a tentativa de envio à API e informa que os campos obrigatórios precisam ser preenchidos

### Requirement: Apresentação visual e carrossel de fotos

O sistema SHALL exibir uma interface de login em duas colunas, contendo um carrossel automático de fotos de animais resgatados na lateral da tela.

#### Scenario: Exibição da tela de login com carrossel
- **WHEN** a tela inicial `/` é carregada
- **THEN** o sistema exibe o formulário de login na coluna direita e inicia a transição automática das fotos do carrossel na coluna esquerda