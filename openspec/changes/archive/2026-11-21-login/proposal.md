# Proposal: Login

## Why

O sistema **Porto Seguro Pet** precisa oferecer uma porta de entrada controlada, segura e acolhedora às suas funcionalidades, contemplando os dois perfis de usuários definidos no projeto: `TUTOR/ADOTANTE` e `ADMINISTRADOR`. A autenticação inicial identifica o perfil de cada usuário, carrega seus dados de sessão e o direciona automaticamente para sua respectiva área de atuação.

## What Changes

- Criar a interface de autenticação única de usuários por e-mail e senha na rota inicial `/`, mantendo o formulário enxuto, direto e alinhado à identidade visual acolhedora do Porto Seguro Pet.
- Adicionar carrossel automático de fotografias de animais resgatados na tela de login para proporcionar uma experiência visual calorosa e alinhada à causa da ONG.
- Integrar a autenticação com a API do Xano (`XANO_LOGIN_URL` e `XANO_ME_URL`) via requisições assíncronas (`httpx`) para validar credenciais, obter o token JWT e recuperar os dados completos do usuário autenticado.
- Identificar o perfil do usuário (`tipo_usuario`) para realizar o direcionamento automático:
  - Usuários do tipo `ADMINISTRADOR` são direcionados para `/administrativo`.
  - Usuários do tipo `TUTOR/ADOTANTE` têm seus dados cadastrais carregados na sessão e são direcionados para `/tutor`.
- Disponibilizar alternância de visibilidade da senha, tratamento claro de credenciais inválidas ou falhas de rede via *toast* e encerramento seguro de sessão (*logout*).

## Capabilities

### New Capabilities

- `user-auth`: autenticação JWT, identificação de perfil (`TUTOR/ADOTANTE` e `ADMINISTRADOR`), carregamento de contexto de sessão, direcionamento por rota e logout via Xano.

### Modified Capabilities

Nenhuma.

## Impact

- **Frontend em Reflex (`ProjetoONG.py`):** implementação da página inicial `/` (`pagina_login`), gerenciamento centralizado de sessão (`LoginState`) e carrossel automático de imagens.
- **Backend em Xano:** consumo dos endpoints de autenticação (`XANO_LOGIN_URL`) e consulta de dados do usuário autenticado (`XANO_ME_URL`).
- **Entidade `USUARIO` (e vínculo com `TUTOR_ADOTANTE`):** utilização dos campos de e-mail, senha, `tipo_usuario` e metadados cadastrais carregados no momento do login.