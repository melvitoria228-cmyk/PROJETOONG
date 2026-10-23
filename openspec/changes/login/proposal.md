# Proposal: Login

## Why

O sistema Porto Seguro Pet precisa oferecer um acesso controlado e acolhedor às suas funcionalidades, contemplando os dois tipos de usuários definidos no projeto: TUTOR/ADOTANTE e ADMINISTRADOR[cite: 1, 19]. A funcionalidade de login é a porta de entrada da aplicação, identificando cada perfil e direcionando-o para a sua respectiva área de atuação[cite: 1].

## What Changes

- Criar a interface de autenticação única de usuários por e-mail e senha na rota inicial `/`[cite: 1].
- Adicionar carrossel automático de fotos de animais na tela de login para proporcionar uma experiência acolhedora[cite: 1].
- Integrar a autenticação com a API do Xano para validar e-mail e senha e obter o token JWT de acesso[cite: 1].
- Identificar o perfil do usuário (`tipo_usuario`) para realizar o direcionamento correto[cite: 1]:
  - Usuários do tipo `ADMINISTRADOR` são direcionados para `/administrativo`[cite: 1].
  - Usuários do tipo `TUTOR/ADOTANTE` são direcionados para `/tutor`[cite: 1].
- Apresentar telas visuais de apoio para solicitação de recuperação e alteração de senha com feedback orientativo por *toast*[cite: 1].

## Capabilities

### New Capabilities

- `user-auth`: autenticação, identificação e direcionamento dos usuários do sistema (`TUTOR/ADOTANTE` e `ADMINISTRADOR`) via Xano com suporte visual a carrossel de imagens[cite: 1, 19].

### Modified Capabilities

Nenhuma.

## Impact

- **Frontend em Reflex (`ProjetoONG.py`):** implementação da página principal `/` com formulário de login, carrossel automático em segundo plano e estados para recuperação/alteração de senha[cite: 1].
- **Backend em Xano:** consumo dos endpoints de autenticação (`XANO_LOGIN_URL`) e de dados do usuário autenticado (`XANO_ME_URL`)[cite: 1].
- **Entidade `USUARIO`:** utilização dos campos e-mail, senha e tipo de usuário definidos na modelagem do sistema[cite: 1, 19].