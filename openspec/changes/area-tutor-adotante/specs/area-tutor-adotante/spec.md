## ADDED Requirements

### Requirement: Exibição da área do Tutor/Adotante

O sistema SHALL disponibilizar uma página inicial para usuários do tipo Tutor/Adotante na rota `/tutor`.

#### Scenario: Acesso à página do Tutor/Adotante

- **WHEN** um usuário do tipo Tutor/Adotante acessa a área correspondente
- **THEN** o sistema apresenta a página inicial da Área do Tutor/Adotante

### Requirement: Cabeçalho superior

O sistema SHALL exibir um cabeçalho superior que identifique a área do Tutor/Adotante e a marca Porto Seguro Pet.

#### Scenario: Exibição do cabeçalho

- **WHEN** a página inicial é exibida
- **THEN** o cabeçalho apresenta a identificação “Área do Tutor/Adotante” e o nome Porto Seguro Pet

### Requirement: Apresentação de boas-vindas

O sistema SHALL exibir uma área de boas-vindas com uma mensagem relacionada à adoção responsável.

#### Scenario: Exibição da mensagem de boas-vindas

- **WHEN** a página inicial é exibida
- **THEN** o usuário visualiza uma saudação e uma mensagem acolhedora

### Requirement: Cartões de navegação

O sistema SHALL apresentar quatro cartões identificados como “Minhas adoções”, “Acompanhamento”, “Meus dados” e “Orientações”.

#### Scenario: Exibição dos cartões

- **WHEN** a página inicial é exibida
- **THEN** os quatro cartões são apresentados com títulos e descrições
- **AND** cada cartão permite acessar sua respectiva página quando a navegação estiver implementada
- **AND** as descrições não apresentam funcionalidades planejadas como se já estivessem disponíveis

### Requirement: Consulta dos processos de adoção

O sistema SHALL permitir que o Tutor/Adotante consulte seus processos de adoção por meio dos dados retornados pelo backend.

#### Scenario: Exibição dos processos de adoção

- **WHEN** o Tutor/Adotante acessa a página “Minhas adoções”
- **THEN** o sistema consulta o endpoint de listagem de adoções do Xano utilizando a autenticação do usuário
- **AND** apresenta os dados retornados pelo backend

#### Scenario: Ausência de processos de adoção

- **WHEN** o backend não retorna processos de adoção para o usuário
- **THEN** o sistema apresenta uma mensagem informando que não há processos para exibir

#### Scenario: Falha na consulta de adoções

- **WHEN** ocorre uma falha na consulta ao backend
- **THEN** o sistema informa que não foi possível carregar os processos de adoção

### Requirement: Identificação do animal relacionado à adoção

O sistema SHOULD apresentar informações que ajudem o Tutor/Adotante a identificar o animal relacionado a cada processo de adoção.

#### Scenario: Identificação do animal

- **WHEN** os dados necessários do animal estiverem disponíveis
- **THEN** o sistema apresenta informações identificadoras, como nome e espécie
- **AND** pode apresentar uma foto quando houver uma imagem disponível

### Requirement: Acompanhamento pós-adoção

O sistema SHALL disponibilizar uma área de acompanhamento pós-adoção para consulta dos registros correspondentes, após a implementação e configuração dos endpoints necessários.

#### Scenario: Consulta do acompanhamento pós-adoção

- **WHEN** o Tutor/Adotante acessa a área de acompanhamento e a funcionalidade está disponível
- **THEN** o sistema apresenta os registros de acompanhamento relacionados às suas adoções

### Requirement: Identidade visual

O sistema SHALL utilizar uma identidade visual baseada nas cores grafite, creme e terracota.

#### Scenario: Exibição da identidade visual

- **WHEN** a página inicial é exibida
- **THEN** a interface utiliza grafite `#3E4149`, creme `#F4E7D5` e terracota `#D78A45` em sua composição visual
