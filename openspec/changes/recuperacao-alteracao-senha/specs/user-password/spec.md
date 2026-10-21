## Propósito

Definir os fluxos seguros de recuperação e alteração da senha de usuários do Porto Seguro Pet, com validação de identidade no Xano.

## ADDED Requirements

### Requirement: Solicitação de recuperação sem revelar a existência da conta

O sistema SHALL permitir que uma pessoa solicite recuperação de senha informando um e-mail e SHALL apresentar resposta pública equivalente independentemente de existir uma conta correspondente.

#### Cenário: Solicitação para e-mail cadastrado

- **WHEN** a pessoa solicita recuperação usando um e-mail cadastrado
- **THEN** o sistema confirma de forma neutra o recebimento da solicitação
- **AND** o Xano envia ao endereço cadastrado uma mensagem com a verificação necessária para continuar

#### Cenário: Solicitação para e-mail não cadastrado

- **WHEN** a pessoa solicita recuperação usando um e-mail não cadastrado
- **THEN** o sistema apresenta resposta equivalente à de uma solicitação recebida
- **AND** não envia mensagem de recuperação nem revela a inexistência da conta

#### Cenário: Falha ou excesso de solicitações

- **WHEN** o serviço de e-mail ou a operação de recuperação está indisponível, ou o limite de tentativas foi atingido
- **THEN** o sistema não revela se a conta existe
- **AND** informa que a solicitação não pôde ser concluída ou que deve ser tentada novamente, sem expor detalhes internos

### Requirement: Verificação antes da redefinição

O sistema SHALL alterar uma senha esquecida somente após o Xano validar uma prova de identidade enviada ao e-mail cadastrado. A prova SHALL ser aleatória, temporária, de uso único, armazenada de forma segura e invalidada após uso, expiração ou substituição por solicitação mais recente.

#### Cenário: Token válido

- **WHEN** a pessoa apresenta um token válido e uma nova senha que atende à política configurada
- **THEN** o Xano atualiza a senha usando o mecanismo seguro de hashing da autenticação
- **AND** invalida o token para usos posteriores
- **AND** o Reflex confirma a operação e permite retornar ao login

#### Cenário: Token ausente, inválido, expirado ou reutilizado

- **WHEN** a pessoa tenta redefinir a senha sem uma prova válida
- **THEN** o Xano rejeita a operação e não altera a senha
- **AND** o Reflex mostra uma mensagem segura para solicitar um novo link quando apropriado

#### Cenário: Nova senha fora da política

- **WHEN** o token é válido, mas a nova senha não atende à política definida no Xano
- **THEN** o Xano rejeita a atualização sem invalidar a identidade como se a senha tivesse sido alterada
- **AND** informa um erro que permita corrigir a nova senha sem revelar dados da conta

### Requirement: Alteração autenticada mediante senha atual

O sistema SHALL permitir que um usuário autenticado altere somente a própria senha, após o Xano confirmar a identidade pelo token da sessão e validar a senha atual com `Check Password`.

#### Cenário: Senha atual válida

- **WHEN** um usuário autenticado informa a senha atual correta e uma nova senha aceita pela política configurada
- **THEN** o Xano atualiza a senha do usuário autenticado usando hashing seguro
- **AND** o Reflex limpa os campos e encerra a sessão local após a confirmação
- **AND** o usuário pode autenticar-se novamente pelo fluxo de login existente

#### Cenário: Senha atual incorreta

- **WHEN** um usuário autenticado informa uma senha atual incorreta
- **THEN** o Xano rejeita a alteração
- **AND** a senha armazenada permanece inalterada
- **AND** o Reflex apresenta uma mensagem genérica sem expor dados de autenticação

#### Cenário: Solicitação sem autenticação ou para outra conta

- **WHEN** uma solicitação de alteração não contém autenticação válida ou tenta indicar uma conta diferente da identidade autenticada
- **THEN** o Xano rejeita a solicitação
- **AND** nenhuma senha é alterada

### Requirement: Proteção de dados sensíveis

O sistema SHALL transmitir credenciais somente por HTTPS e SHALL impedir que senhas, tokens de sessão, tokens de recuperação, cabeçalhos de autorização, links de recuperação ou corpos sensíveis sejam incluídos em logs ou respostas públicas.

#### Cenário: Erro de integração

- **WHEN** ocorre uma falha HTTP, de conexão, de formato ou de envio de e-mail em qualquer fluxo de senha
- **THEN** os logs registram somente informações operacionais não sensíveis necessárias à investigação
- **AND** a resposta ao usuário não inclui senha, token, cabeçalho, corpo da API ou URL sensível

### Requirement: Preservação do login existente

O sistema SHALL preservar o fluxo atual de autenticação por `XANO_LOGIN_URL` e consulta de identidade por `XANO_ME_URL`, incluindo o direcionamento do administrador para `/administrativo` e do tutor/adotante para `/tutor`.

#### Cenário: Login após recuperação ou troca

- **WHEN** um usuário autentica com a nova senha válida
- **THEN** o fluxo de login existente identifica seu tipo de usuário
- **AND** direciona-o para a área correspondente

#### Cenário: Login com a senha anterior

- **WHEN** um usuário tenta autenticar com a senha anterior depois de uma redefinição ou alteração concluída
- **THEN** o login não autentica com a senha anterior