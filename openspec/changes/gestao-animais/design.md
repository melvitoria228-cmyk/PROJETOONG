## Context

O projeto Porto Seguro Pet utiliza Reflex no frontend e Xano no backend. A tabela `ANIMAL` e seus endpoints de consulta, cadastro, edição e exclusão já existem no grupo de API `PortoSeguroPet`.

A aplicação possui uma estrutura de autenticação e uma área administrativa implementadas em `ProjetoONG.py`. A nova tela deverá aproveitar essa estrutura, mantendo o funcionamento das rotas e dos demais recursos existentes.

Os requisitos funcionais desta mudança estão definidos em `specs/gestao-animais/spec.md`.

## Goals / Non-Goals

**Goals:**

* Integrar a tela de Gestão de Animais aos endpoints existentes do Xano.
* Reutilizar a estrutura de componentes, estado e navegação já adotada na aplicação Reflex.
* Manter a identidade visual administrativa definida para o projeto.
* Tratar resultados e falhas das operações sem apresentar mensagens de sucesso indevidas.
* Respeitar os campos, os status e os relacionamentos já definidos para os animais.

**Non-Goals:**

* Criar uma nova tabela `ANIMAL` ou duplicar os endpoints existentes.
* Alterar a autenticação ou substituir o mecanismo de login.
* Implementar módulos de outros processos da ONG nesta mudança.
* Adicionar bibliotecas ou dependências sem necessidade.
* Modificar a estrutura do banco de dados sem justificativa e validação prévias.

## Decisions

### 1. Reutilizar a arquitetura existente

A tela será implementada no arquivo `ProjetoONG.py`, aproveitando as rotas, os componentes e os padrões de estado já utilizados no projeto.

**Alternativa considerada:** criar um módulo separado para a tela. Essa opção pode facilitar a organização futura, mas não será adotada nesta etapa sem necessidade comprovada, para manter a implementação incremental e simples.


### 2. Utilizar o Xano como fonte dos dados

As operações de consulta, cadastro, edição e exclusão utilizarão os endpoints existentes da tabela `ANIMAL`, no grupo de API `PortoSeguroPet`.

A URL-base da API de animais deverá ser configurada por meio da variável de ambiente `XANO_ANIMAL_URL`, definida no arquivo `.env`. Essa configuração deverá seguir o mecanismo já utilizado pelo projeto, sem inserir URLs de configuração ou credenciais diretamente no código-fonte.

O arquivo `.env` deverá permanecer protegido pelo `.gitignore`. Um arquivo `.env.example` poderá documentar os nomes das variáveis necessárias, sem incluir valores reais ou informações sensíveis.

Os endpoints atuais não exigem autenticação. Por isso, as operações de escrita deverão ter seu acesso restringido no Xano antes da disponibilização pública do sistema. A integração deverá respeitar as regras de acesso configuradas no backend.

**Alternativa considerada:** manter os animais apenas em uma lista local do frontend. Essa opção não será adotada porque os registros precisam permanecer armazenados no backend e disponíveis entre sessões.

#
### 3. Preservar o modelo de dados existente

A interface utilizará os campos de negócio já definidos para a entidade `ANIMAL` no Xano:

- `nome`: texto.
- `especie`: texto.
- `raca`: texto.
- `idade_estimada`: número inteiro.
- `sexo`: texto.
- `porte`: texto.
- `condicao_saude`: texto.
- `status_atual`: texto.
- `data_resgate`: data.

Os campos de negócio deverão ser preenchidos conforme as regras de obrigatoriedade configuradas no backend. Os campos de identificação e controle, como `id` e `created_at`, serão tratados como dados gerenciados pelo sistema e não deverão ser editados pelo usuário.

Os campos com opções padronizadas utilizarão as seguintes alternativas:

- `especie`: Cão, Gato e Outros.
- `sexo`: Macho, Fêmea e Não identificado.
- `porte`: Mini, Pequeno, Médio e Grande.
- `status_atual`: Disponível, Em Lar Temporário, Em Processo de Adoção, Adotado e Falecido.

Antes da implementação, os valores já armazenados no Xano deverão ser conferidos. A interface deverá preservar os registros existentes e evitar divergências de escrita ou acentuação entre as opções exibidas e os valores enviados ao backend.

**Alternativa considerada:** criar campos adicionais ou modificar os tipos existentes para facilitar a interface. Essa opção será evitada para não introduzir divergências entre o frontend e o backend.


### 4. Separar os estados de consulta e edição

A implementação deverá distinguir os dados recebidos do Xano dos valores temporários preenchidos no formulário.

Após uma operação bem-sucedida, a lista deverá ser atualizada com os dados confirmados pelo backend. Em caso de falha, os dados anteriormente confirmados deverão ser preservados, sem apresentar as alterações como salvas.

**Alternativa considerada:** atualizar somente a interface antes de confirmar a operação no Xano. Essa abordagem pode apresentar informações incorretas quando houver falhas e, por isso, não será utilizada como comportamento definitivo.


### 5. Tratar a exclusão com confirmação

A exclusão deverá solicitar confirmação do usuário antes de enviar a operação ao Xano.

O registro somente deverá ser removido da lista após a confirmação de sucesso pelo backend. Se o usuário cancelar a exclusão, nenhuma solicitação deverá ser enviada.

Caso o backend impeça a exclusão por causa de relacionamentos, regras de negócio ou falha de comunicação, o registro deverá permanecer na interface e uma mensagem deverá informar que a exclusão não foi concluída.

**Alternativa considerada:** excluir imediatamente ao clicar no botão. Essa opção aumenta o risco de exclusões acidentais e será evitada.

### 6. Manter a identidade visual administrativa

A tela seguirá uma paleta própria para a área administrativa, diferenciando-a visualmente da área do tutor/adotante.

As cores principais serão:

* **Marrom (`#57463B`):** menu lateral, títulos e elementos de maior destaque.
* **Areia (`#F1E4D2`):** fundo da página e áreas de respiro.
* **Terracota (`#B66A4B`):** botões principais e ações importantes.
* **Caramelo claro (`#D7B99A`):** bordas, detalhes e destaques suaves.

Os status dos animais utilizarão cores complementares para facilitar a identificação:

* **Disponível para adoção:** verde suave.
* **Em lar temporário:** amarelo suave.
* **Em processo de adoção:** azul suave.
* **Adotado:** lilás suave.
* **Falecido:** cinza neutro.

As cores dos status deverão ser acompanhadas de texto legível, para que a situação do animal não seja identificada exclusivamente pela cor.

A interface deverá priorizar a leitura dos registros, a organização das informações e o acesso às ações de consulta e manutenção.

## Risks / Trade-offs

* **Falha de comunicação com o Xano** → apresentar uma mensagem clara e não indicar que a operação foi concluída.
* **Divergência entre os campos do formulário e o backend** → conferir os nomes, tipos e valores aceitos pelos endpoints antes da implementação.
* **Exclusão bloqueada por relacionamentos** → tratar a resposta do backend e preservar o registro.
* **Alterações involuntárias em recursos existentes** → modificar somente o necessário em `ProjetoONG.py` e testar o login e as rotas já existentes.
* **Exposição de credenciais ou tokens** → reutilizar a configuração segura existente e evitar registrar dados sensíveis em mensagens de erro.

## Migration Plan

1. Confirmar a configuração dos endpoints e os campos existentes no Xano.
2. Implementar a tela e as operações na aplicação Reflex.
3. Testar consulta, cadastro, visualização, edição e exclusão, incluindo cenários de falha.
4. Verificar se o login e as demais rotas continuam funcionando.
5. Se a implementação apresentar problemas, reverter as alterações específicas desta mudança em `ProjetoONG.py`, preservando a configuração existente do Xano.

