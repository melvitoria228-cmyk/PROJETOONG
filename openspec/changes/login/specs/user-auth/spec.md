## Purpose

Permitir que usuários autorizados acessem o sistema Porto Seguro Pet de acordo com seu tipo de usuário, garantindo um acesso simples e controlado às áreas correspondentes.

## ADDED Requirements

### Requirement: Acesso com credenciais válidas

O sistema SHALL permitir o acesso quando o usuário informar um e-mail e uma senha correspondentes a uma conta válida.

#### Scenario: Login com credenciais válidas

- **WHEN** o usuário informar e-mail e senha válidos
- **THEN** o sistema deve permitir o acesso ao sistema

### Requirement: Tratamento de credenciais inválidas

O sistema SHALL impedir o acesso quando o e-mail ou a senha informados não corresponderem a uma conta válida.

#### Scenario: Login com credenciais inválidas

- **WHEN** o usuário informar credenciais inválidas
- **THEN** o sistema deve impedir o acesso e informar que as credenciais não são válidas

### Requirement: Identificação do tipo de usuário

O sistema SHALL identificar o tipo de usuário após um login válido, considerando os tipos TUTOR/ADOTANTE e ADMINISTRADOR definidos no sistema.

#### Scenario: Acesso de TUTOR/ADOTANTE

- **WHEN** um usuário do tipo TUTOR/ADOTANTE realizar login com credenciais válidas
- **THEN** o sistema deve identificar o usuário como TUTOR/ADOTANTE

#### Scenario: Acesso de ADMINISTRADOR

- **WHEN** um usuário do tipo ADMINISTRADOR realizar login com credenciais válidas
- **THEN** o sistema deve identificar o usuário como ADMINISTRADOR

### Requirement: Campos obrigatórios do login

O sistema SHALL exigir o preenchimento do e-mail e da senha para realizar uma tentativa de login.

#### Scenario: Campos não preenchidos

- **WHEN** o usuário tentar realizar login sem informar e-mail ou senha
- **THEN** o sistema deve impedir a tentativa de acesso e informar que os campos obrigatórios precisam ser preenchidos
