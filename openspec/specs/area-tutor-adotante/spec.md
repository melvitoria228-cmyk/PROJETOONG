# area-tutor-adotante Specification

## Purpose
TBD - created by archiving change area-tutor-adotante. Update Purpose after archive.

## Requirements

### Requirement: Painel Enxuto do Tutor

O sistema SHALL focar a experiência do Tutor/Adotante na rota `/tutor` na exibição clara do status das solicitações e no gerenciamento cadastral simplificado.

#### Scenario: Visualização e Gestão Prioritária
- **WHEN** o tutor acessa a rota `/tutor`
- **THEN** o sistema apresenta de forma direta o feed de suas solicitações com o indicador visual de etapas (Stepper) e nome do animal
- **AND** disponibiliza o formulário de atualização de perfil em `/meus-dados` integrado via `PATCH` ao Xano.

### Requirement: Exibição da área do Tutor/Adotante

O sistema SHALL disponibilizar uma página inicial para usuários do tipo Tutor/Adotante na rota `/tutor`.

#### Scenario: Acesso à página do Tutor/Adotante

- **WHEN** um usuário do tipo Tutor/Adotante realiza login com sucesso
- **THEN** o sistema o redireciona automaticamente para a rota `/tutor`
- **AND** apresenta o painel inicial da Área do Tutor/Adotante

### Requirement: Cabeçalho superior e navegação

O sistema SHALL exibir um cabeçalho superior que identifique a marca Porto Seguro Pet e permita o encerramento da sessão (*logout*).

#### Scenario: Exibição do cabeçalho e logout

- **WHEN** a página da Área do Tutor é exibida
- **THEN** o cabeçalho apresenta a identificação da marca Porto Seguro Pet
- **AND** disponibiliza o botão/link "Sair" que limpa os dados de sessão e redireciona para a tela inicial

### Requirement: Apresentação de boas-vindas e resumo do perfil

O sistema SHALL exibir uma mensagem de boas-vindas acolhedora e um bloco de resumo dos dados do tutor logado.

#### Scenario: Exibição da mensagem de boas-vindas e perfil

- **WHEN** a página inicial `/tutor` é exibida
- **THEN** o usuário visualiza a mensagem de boas-vindas
- **AND** visualiza o resumo de seus dados cadastrais (nome, e-mail e tipo de perfil)

### Requirement: Cartões de navegação e serviços

O sistema SHALL apresentar três cartões/blocos de atalho para serviços identificados como “Meus dados”, “Acompanhamento” e “Orientações”.

#### Scenario: Exibição e navegação dos cartões

- **WHEN** a página inicial é exibida
- **THEN** os três cartões são apresentados com seus respectivos títulos e descrições
- **AND** o clique em "Meus dados" direciona para a página `/meus-dados`
- **AND** o clique em "Acompanhamento" direciona para a página `/acompanhamento`
- **AND** o clique em "Orientações" direciona para a página `/orientacoes`

### Requirement: Consulta e exibição dos processos de adoção

O sistema SHALL permitir que o Tutor/Adotante consulte seus processos de adoção em um feed dinâmico integrado ao Xano.

#### Scenario: Exibição dos processos de adoção

- **WHEN** o Tutor/Adotante acessa a rota `/tutor`
- **THEN** o sistema consulta o endpoint GET de listagem de processos de adoção do Xano utilizando o token de autenticação
- **AND** apresenta as solicitações de adoção cadastradas para aquele usuário

#### Scenario: Ausência de processos de adoção

- **WHEN** o backend não retorna processos de adoção para o usuário
- **THEN** o sistema apresenta um painel informativo de estado vazio indicando que não há solicitações em andamento

#### Scenario: Falha na consulta de adoções

- **WHEN** ocorre uma falha na consulta ao backend
- **THEN** o sistema informa ao usuário que não foi possível carregar os processos de adoção

### Requirement: Identificação do animal relacionado à adoção

O sistema SHALL apresentar o nome do animal relacionado a cada processo de adoção, utilizando os dados obtidos via Add-on do Xano.

#### Scenario: Identificação do animal por nome

- **WHEN** os dados da solicitação de adoção são retornados pela API com o Add-on do animal
- **THEN** o sistema exibe o nome real do animal no cabeçalho do cartão da solicitação
- **AND** caso o nome não esteja disponível, exibe uma identificação fallback (`Animal #ID` ou `Pet em Processo`)

### Requirement: Indicador visual de progresso da adoção (Stepper)

O sistema SHALL exibir um indicador gráfico em etapas (1. Análise, 2. Aprovação, 3. Concluído) e uma explicação textual para o status do processo.

#### Scenario: Exibição do progresso por etapa

- **WHEN** um processo de adoção é exibido
- **THEN** o sistema destaca os passos do indicador visual de acordo com o `status_processo` (`Em análise`, `Aprovada`, `Adoção efetivada`, etc.)
- **AND** apresenta uma caixa de texto explicativa detalhando a fase atual para o tutor

### Requirement: Edição dos dados cadastrais do Tutor

O sistema SHALL permitir que o Tutor/Adotante visualize e atualize seus dados pessoais na rota `/meus-dados`.

#### Scenario: Atualização dos dados cadastrais

- **WHEN** o tutor altera suas informações (nome, CPF, telefone, tipo de residência, endereço) na página `/meus-dados` e clica em "Salvar Alterações"
- **THEN** o sistema envia uma requisição `PATCH` com os novos dados ao endpoint de atualização do tutor no Xano
- **AND** exibe uma mensagem de confirmação (*toast*) indicando o sucesso da operação

### Requirement: Acompanhamento pós-adoção

O sistema SHALL disponibilizar a página `/acompanhamento` para consulta dos relatórios de acompanhamento pós-adoção.

#### Scenario: Consulta do acompanhamento pós-adoção

- **WHEN** o Tutor/Adotante acessa a rota `/acompanhamento`
- **THEN** o sistema consulta o endpoint de acompanhamento do Xano e exibe o histórico de visitas e observações registradas pela ONG

### Requirement: Guia de Orientações

O sistema SHALL disponibilizar a página `/orientacoes` com conteúdos educativos sobre guarda responsável.

#### Scenario: Exibição das orientações

- **WHEN** o Tutor/Adotante acessa a rota `/orientacoes`
- **THEN** o sistema exibe as orientações de adaptação, saúde e segurança do pet

### Requirement: Identidade visual

O sistema SHALL utilizar uma identidade visual baseada nas cores grafite, creme e terracota.

#### Scenario: Exibição da identidade visual

- **WHEN** as páginas da Área do Tutor são exibidas
- **THEN** a interface utiliza grafite `#2D3142` / `#3E4149`, creme `#FFF7ED` / `#F4E7D5` e terracota `#D78A45` em sua composição visual
