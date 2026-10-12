## Why

O sistema Porto Seguro Pet precisa oferecer um acesso controlado às suas funcionalidades, contemplando os dois tipos de usuários definidos no projeto: TUTOR/ADOTANTE e ADMINISTRADOR. A mudança cria a base da funcionalidade de login, permitindo que cada tipo de usuário acesse a área correspondente do sistema.

## What Changes

- Criar a capacidade de autenticação de usuários por e-mail e senha.
- Permitir o acesso dos usuários do tipo TUTOR/ADOTANTE.
- Permitir o acesso dos usuários do tipo ADMINISTRADOR.
- Identificar o tipo de usuário após o acesso para direcioná-lo à área correspondente.
- Criar a base da tela de login no frontend.
- Não implementar ainda funcionalidades específicas das áreas do administrador ou do tutor.

## Capabilities

### New Capabilities

- `user-auth`: autenticação e acesso dos usuários do sistema, contemplando TUTOR/ADOTANTE e ADMINISTRADOR.

### Modified Capabilities

Nenhuma.

## Impact

- Frontend em Reflex: criação da interface de login.
- Backend em Xano: posteriormente será utilizado para autenticação e identificação do tipo de usuário.
- Entidade `USUARIO`: utilização de e-mail, senha e tipo de usuário definidos na documentação do sistema.
