# Design: Login

## Context

O projeto **Porto Seguro Pet** utiliza **Reflex** no frontend e **Xano** no backend. A entidade `USUARIO` concentra os dados necessários para o acesso ao sistema, incluindo e-mail, senha e `tipo_usuario` (`ADMINISTRADOR` ou `TUTOR/ADOTANTE`). Esta change utiliza essa estrutura para implementar o acesso autenticado via JWT e o direcionamento por perfil sem criar uma estrutura paralela de autenticação.

## Goals / Non-Goals

**Goals:**
- Criar uma única interface de login enxuta e acolhedora na rota inicial `/` para os usuários do sistema.
- Exibir um carrossel visual automático com fotos de animais na lateral da tela de login para enriquecer a experiência inicial.
- Utilizar o Xano como backend responsável pela autenticação via variáveis de ambiente (`XANO_LOGIN_URL` e `XANO_ME_URL`).
- Identificar o `tipo_usuario` para diferenciar `TUTOR/ADOTANTE` e `ADMINISTRADOR`, carregar o contexto da sessão (incluindo vínculo com `TUTOR_ADOTANTE`) e direcionar para suas respectivas áreas após o login.
- Disponibilizar alternância de visibilidade da senha, feedback claro via `rx.toast` e encerramento seguro de sessão (`LoginState.sair`).
- Centralizar o controle de sessão no estado global do Reflex (`LoginState`).

**Non-Goals:**
- Incluir botões ou fluxos de recuperação e alteração de senha na tela de login nesta entrega, mantendo a interface focada na autenticação direta.
- Implementar formulário de auto-cadastro de novos usuários nesta change.
- Expor funcionalidades específicas de adoção ou administração na tela inicial `/`.

## Decisions

### 1. Uma única tela de login com carrossel visual

Será utilizada uma única tela na rota `/` para os dois perfis de usuário. A interface divide-se em duas colunas: à esquerda apresenta um carrossel automático de fotografias de animais resgatados, e à direita contém o formulário direto de autenticação (`email` e `senha`, com alternância de visibilidade da senha) sobre fundo personalizado.

### 2. Carrossel automático assíncrono no Reflex

O carrossel utiliza imagens de animais configuradas no `LoginState` (`fotos_carrossel`), com transição automática por tempo executada em segundo plano via evento assíncrono (`iniciar_carrossel_automatico` disparado no `on_load` da rota `/`), além de controles manuais de navegação entre os slides.

### 3. Xano como backend de autenticação JWT

A autenticação é realizada pelo backend em Xano via requisição assíncrona `POST` (`httpx`) no endpoint configurado em `XANO_LOGIN_URL`. O token JWT retornado é armazenado na sessão (`LoginState.token`) e imediatamente utilizado na consulta `GET` em `XANO_ME_URL` para identificar o `tipo_usuario` e capturar os dados cadastrais vinculados à tabela `TUTOR_ADOTANTE`.

### 4. Identificação e direcionamento pelo tipo de usuário

Após uma autenticação válida, o sistema normaliza e avalia o `tipo_usuario` para redirecionar o usuário:
- `administrador` → redirecionado para a rota `/administrativo`.
- `tutor/adotante` → redirecionado para a rota `/tutor`.
- Tipo ausente ou não reconhecido → mantém o usuário na tela `/` e exibe alerta orientativo via `rx.toast` sem conceder acesso às rotas restritas.

## Risks / Trade-offs

- **Dependência do backend Xano** → A autenticação depende da disponibilidade e configuração correta das variáveis `XANO_LOGIN_URL` e `XANO_ME_URL` no `.env`; falhas de rede ou credenciais inválidas são tratadas com mensagens claras via `rx.toast`.
- **Disponibilidade das imagens externas do carrossel** → O carrossel depende do carregamento das URLs configuradas; mantém-se estrutura visual consistente mesmo em conexões lentas.
- **Ausência de fluxo de redefinição de senha na tela inicial** → Opção intencional para evitar links sem integração real de e-mail nesta entrega; a redefinição de credenciais permanece administrada diretamente via suporte/banco de dados.

## Migration Plan

1. Manter a página `pagina_login` registrada e ativa na rota principal `/` em `ProjetoONG.py` com `on_load=LoginState.iniciar_carrossel_automatico`.
2. Garantir que `XANO_LOGIN_URL` e `XANO_ME_URL` estejam configuradas no `.env` e documentadas no `.env.example`.
3. Validar em ambiente local os fluxos de login como `ADMINISTRADOR` (`/administrativo`), login como `TUTOR/ADOTANTE` (`/tutor`), credenciais inválidas e logout (`LoginState.sair`).

## Open Questions

Nenhuma.