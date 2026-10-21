## Contexto

O frontend é implementado em Reflex e o Xano é responsável por autenticação e persistência. O login atual usa as configurações `XANO_LOGIN_URL` e `XANO_ME_URL`; esta change não altera esses fluxos. As operações de senha descritas abaixo ainda precisam ser configuradas no Xano: seus caminhos e URLs reais não estão definidos nesta change.

## Objetivos e não objetivos

**Objetivos:**
- Criar recuperação com comprovação de controle do e-mail, separando solicitação de redefinição.
- Criar alteração de senha vinculada à identidade autenticada e à senha atual.
- Manter validação, hashing, persistência e decisões de autorização no Xano.
- Evitar enumeração de contas e exposição de credenciais, tokens ou dados pessoais em logs.
- Preservar o fluxo de login e o direcionamento para administrador e tutor/adotante.

**Não objetivos:**
- Inventar ou presumir endpoints Xano existentes.
- Redefinir senha apenas com base no e-mail informado.
- Alterar arquitetura, cadastro ou regras de acesso por tipo de usuário.
- Definir uma política numérica de senha sem confirmar a política configurada no Xano.

## Decisões

### Recuperação em duas etapas

O Reflex solicita o início da recuperação usando o e-mail. O Xano responde com mensagem equivalente exista ou não a conta, aplica limites de tentativa e, quando apropriado, envia um link de verificação. A redefinição só é aceita após o Xano validar um token aleatório, temporário, de uso único e associado à conta. O token deve ser armazenado no backend de forma segura, preferencialmente como hash, e invalidado após uso, expiração ou emissão de uma solicitação mais recente.

O tempo de validade, o limite de solicitações e a política para tokens anteriores são configurações a definir no Xano antes da implementação. O frontend não deve receber confirmação que permita inferir a existência da conta.

### Alteração autenticada

O Reflex envia a senha atual e a nova senha pela conexão HTTPS usando o token de autenticação já obtido pelo login. O Xano identifica o usuário exclusivamente pelo contexto autenticado, valida a senha atual com `Check Password` e persiste a nova senha usando o mecanismo seguro de hashing da autenticação. O request não deve aceitar um identificador de usuário arbitrário para escolher a conta a alterar.

Após o sucesso, o Reflex limpa os campos e encerra a sessão local, retornando ao login. O Xano deve definir se revoga também outras sessões e documentar a compatibilidade dessa decisão com o mecanismo atual de tokens.

### Responsabilidades do Reflex e do Xano

O Reflex apresenta formulários, valida campos obrigatórios, chama as operações configuradas e mostra mensagens neutras. Não valida identidade por conta própria, não compara senha com dados locais e não grava senhas ou tokens de recuperação em persistência local.

O Xano valida identidade e autorização, aplica limites de tentativas e política de senha, envia e-mail, valida/invalida tokens e atualiza o hash. Os contratos de entrada/saída e as URLs reais serão registrados após configurar as operações; os nomes e caminhos ainda não são definidos aqui.

### Configuração do frontend

Depois da criação das operações no Xano, adicionar variáveis de ambiente para as URLs de solicitação, confirmação e alteração autenticada. Os nomes finais serão definidos na implementação e documentados em `.env.example`; nenhuma URL será adicionada ao repositório como segredo.

### Logs e respostas

Não registrar senhas, tokens, cabeçalhos de autorização, corpo de requisição/resposta, e-mail completo nem links de recuperação. Logs operacionais podem conter etapa, status HTTP e classe da falha, sem conteúdo sensível. Respostas exibidas ao usuário não devem revelar a existência da conta nem detalhes internos do Xano.

## Fluxos

### Recuperar senha

1. A pessoa abre “Esqueci minha senha” na tela de login e informa o e-mail.
2. O Reflex envia a solicitação ao Xano e apresenta uma confirmação neutra.
3. Quando a conta puder ser recuperada, o Xano envia a mensagem com um link contendo a prova temporária.
4. A pessoa abre o link, informa a nova senha e confirma a redefinição.
5. O Xano valida o token e a política de senha, atualiza o hash e invalida o token. O Reflex confirma o resultado e oferece retorno ao login.

### Alterar senha

1. O usuário autenticado abre a opção de segurança da conta, disponível para os tipos de usuário já suportados.
2. Informa senha atual, nova senha e confirmação da nova senha.
3. O Reflex envia a senha atual e a nova ao Xano com o token da sessão.
4. O Xano valida a identidade e a senha atual, verifica a política de senha e atualiza o hash.
5. O Reflex limpa os campos, encerra a sessão local e direciona ao login.

## Riscos e mitigação

* **Enumeração de contas:** respostas públicas equivalentes e limites de tentativa no Xano.
* **Roubo ou repetição de token:** token aleatório, com validade limitada, uso único, armazenamento seguro e invalidação no uso ou expiração.
* **Alteração de conta alheia:** obter o usuário do contexto autenticado e não de um ID informado pelo cliente.
* **Exposição de segredo:** HTTPS, ausência de segredos em logs/respostas e limpeza dos campos no frontend após o fluxo.
* **Dependência de e-mail ou backend:** tratar indisponibilidade sem informar se uma conta existe e permitir nova solicitação respeitando limites.
* **Sessões previamente emitidas:** decidir e testar no Xano a revogação após redefinição/troca; a sessão local será encerrada após alteração autenticada.

## Plano de implementação

1. Definir e implementar no Xano os contratos, configurações de e-mail, política de senha, limites, validade e revogação.
2. Configurar as URLs reais no ambiente Reflex e documentar somente os nomes das variáveis em `.env.example`.
3. Implementar os formulários e estados Reflex, mantendo o login atual inalterado.
4. Testar fluxos positivos e negativos, revisar logs e executar validações de sintaxe e OpenSpec.

## Questões em aberto

* Qual é a política de senha atualmente configurada no Xano e qual mensagem o usuário deve receber quando a nova senha não a atender?
* Qual provedor de e-mail e URL de retorno serão usados para o link de recuperação?
* Qual é o tempo de validade e o limite de tentativas para solicitações e tokens?
* O Xano consegue revogar todos os tokens de sessão após redefinição ou alteração? Se não, qual será o prazo máximo de validade das sessões existentes?
* Onde ficará a opção de alteração de senha na interface atual, que ainda não possui tela de configurações de conta?