## ADDED Requirements

### Requirement: Exibição da área do Tutor/Adotante

O sistema SHALL disponibilizar uma página inicial para usuários do tipo Tutor/Adotante na rota `/tutor`.

#### Scenario: Acesso à página do Tutor/Adotante

* **WHEN** a aplicação acessa a rota `/tutor`
* **THEN** o sistema apresenta a página inicial da Área do Tutor/Adotante

### Requirement: Cabeçalho superior

O sistema SHALL exibir um cabeçalho superior que identifique a área do Tutor/Adotante e a marca Porto Seguro Pet.

#### Scenario: Exibição do cabeçalho

* **WHEN** a página inicial é exibida
* **THEN** o cabeçalho apresenta a identificação “Área do Tutor/Adotante” e o nome Porto Seguro Pet

### Requirement: Apresentação de boas-vindas

O sistema SHALL exibir uma área de boas-vindas com uma mensagem relacionada à adoção responsável.

#### Scenario: Exibição da mensagem de boas-vindas

* **WHEN** a página inicial é exibida
* **THEN** o usuário visualiza uma saudação e uma mensagem acolhedora

### Requirement: Cartões informativos

O sistema SHALL apresentar quatro cartões visuais identificados como “Minhas adoções”, “Acompanhamento”, “Meus dados” e “Orientações”.

#### Scenario: Exibição dos cartões

* **WHEN** a página inicial é exibida
* **THEN** os quatro cartões são apresentados com títulos e descrições
* **AND** os cartões não simulam funcionalidades que ainda não foram implementadas

### Requirement: Identidade visual

O sistema SHALL utilizar uma identidade visual baseada nas cores grafite, creme e terracota.

#### Scenario: Exibição da identidade visual

* **WHEN** a página inicial é exibida
* **THEN** a interface utiliza grafite `#3E4149`, creme `#F4E7D5` e terracota `#D78A45` em sua composição visual
