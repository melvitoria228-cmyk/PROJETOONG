# Spec: Login

## Purpose

Permitir que usuários autorizados acessem o sistema **Porto Seguro Pet** na rota `/` de acordo com seu perfil (`ADMINISTRADOR` ou `TUTOR/ADOTANTE`), garantindo autenticação segura via JWT, carregamento de contexto da sessão e uma experiência visual acolhedora.

## ADDED Requirements

### Requirement: Acesso com credenciais válidas e direcionamento por perfil

O sistema SHALL permitir o acesso quando o usuário informar um e-mail e uma senha correspondentes a uma conta válida no Xano (`XANO_LOGIN_URL`), consultando os dados do usuário (`XANO_ME_URL`) e redirecionando-o automaticamente para a área correspondente ao seu perfil.

#### Scenario: Login com credenciais válidas do tipo ADMINISTRADOR
- **WHEN** o usuário informar e-mail e senha válidos de uma conta do tipo `ADMINISTRADOR`
- **THEN** o sistema autentica o usuário via Xano, armazena o token JWT na sessão (`LoginState.token`) e redireciona automaticamente para a rota `/administrativo`

#### Scenario: Login com credenciais válidas do tipo TUTOR/ADOTANTE
- **WHEN** o usuário informar e-mail e senha válidos de uma conta do tipo `TUTOR/ADOTANTE`
- **THEN** o sistema autentica o usuário via Xano, armazena o token JWT e os dados cadastrais vinculados ao tutor na sessão, e redireciona automaticamente para a rota `/tutor`

### Requirement: Tratamento de credenciais inválidas, perfil desconhecido e falhas

O sistema SHALL impedir o acesso às áreas restritas quando o e-mail ou a senha forem inválidos, quando o perfil não for reconhecido ou quando ocorrer falha de comunicação com o backend.

#### Scenario: Login com credenciais inválidas
- **WHEN** o usuário informar e-mail ou senha incorretos
- **THEN** o sistema impede o acesso e exibe uma mensagem clara de erro via *toast*

#### Scenario: Perfil de usuário não reconhecido
- **WHEN** o Xano autenticar a conta mas retornar um `tipo_usuario` diferente de `ADMINISTRADOR` e `TUTOR/ADOTANTE`
- **THEN** o sistema mantém o usuário na rota `/` sem conceder acesso às rotas restritas e exibe um alerta via *toast*

#### Scenario: Falha de comunicação com o Xano
- **WHEN** ocorrer erro de rede ou indisponibilidade dos endpoints de autenticação
- **THEN** o sistema interrompe o carregamento e informa ao usuário via *toast* que não foi possível concluir o login

### Requirement: Campos obrigatórios e visibilidade da senha

O sistema SHALL exigir o preenchimento de e-mail e senha antes de enviar a requisição de autenticação e permitir alternar a visibilidade do campo de senha.

#### Scenario: Campos obrigatórios não preenchidos
- **WHEN** o usuário tentar realizar login sem informar e-mail ou senha
- **THEN** o sistema impede o envio à API e informa via *toast* que os campos obrigatórios precisam ser preenchidos

#### Scenario: Alternar exibição da senha
- **WHEN** o usuário acionar o controle de visibilidade no campo de senha
- **THEN** o sistema alterna a exibição dos caracteres entre oculto (`password`) e visível (`text`)

### Requirement: Apresentação visual e carrossel automático de fotos

O sistema SHALL exibir uma interface de login enxuta em duas colunas na rota `/`, contendo um carrossel automático de fotos de animais resgatados na lateral da tela.

#### Scenario: Exibição da tela de login com carrossel
- **WHEN** a tela inicial `/` é carregada
- **THEN** o sistema exibe o formulário direto de autenticação na coluna direita (sem links ou botões de alteração de senha) e inicia a transição automática das fotos do carrossel na coluna esquerda via `on_load`

### Requirement: Encerramento de sessão (Logout)

O sistema SHALL permitir que usuários autenticados encerrem sua sessão de forma segura a partir das áreas internas.

#### Scenario: Realizar logout do sistema
- **WHEN** o usuário acionar o botão "Sair" (`LoginState.sair`) na Área Administrativa ou na Área do Tutor
- **THEN** o sistema limpa o token JWT e os dados de usuário armazenados na sessão e redireciona para a tela inicial `/`