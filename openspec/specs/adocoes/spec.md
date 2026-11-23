# adocoes Specification

## Purpose
Definir os requisitos funcionais da tela administrativa de Gestão de Adoções (`/adocoes`), permitindo que a equipe da ONG tria, acompanhe e atualize os processos de adoção em uma interface Master-Detail auditável integrada ao backend Xano.

## Requirements

### Requirement: Consulta e Carregamento Automático dos Processos de Adoção

O sistema MUST carregar automaticamente os processos de adoção cadastrados no Xano ao acessar a rota `/adocoes` (`on_load`), utilizando o token JWT da sessão administrativa.

#### Scenario: Carregamento bem-sucedido dos processos de adoção
- **WHEN** o usuário administrativo acessa a rota `/adocoes`
- **THEN** o sistema MUST consultar os registros autenticados no Xano, apresentar a fila de solicitações com identificação do solicitante e do animal relacionado, e selecionar automaticamente o primeiro item disponível para exibição no painel de detalhes.

#### Scenario: Ausência de processos de adoção ou falha de comunicação
- **WHEN** não houver solicitações cadastradas ou ocorrer falha de comunicação com o Xano
- **THEN** o sistema MUST exibir um estado vazio informativo ou notificar o erro via *toast* sem quebrar a interface.

### Requirement: Estrutura Master-Detail (Split View 35/65)

O sistema MUST exibir um layout dividido no padrão Master-Detail (~35% lista à esquerda e ~65% detalhes à direita) integrado ao menu lateral administrativo (`sidebar_administracao`).

#### Scenario: Filtragem e seleção na lista Master
- **WHEN** o usuário digita um termo na barra de pesquisa (nome do solicitante ou do pet) ou altera o filtro de status
- **THEN** a lista Master da coluna esquerda MUST atualizar dinamicamente para exibir apenas as solicitações correspondentes.

#### Scenario: Seleção de um item da lista
- **WHEN** o usuário clica em um cartão da coluna esquerda
- **THEN** o cartão selecionado MUST receber destaque visual e a coluna direita MUST exibir imediatamente os detalhes completos da solicitação selecionada (dados do animal, dados do tutor e questionário de triagem).

### Requirement: Imutabilidade e Auditabilidade de Dados Sensíveis

O sistema MUST aplicar restrições de somente leitura em campos sensíveis e declaratórios para preservar a auditabilidade do processo de adoção.

#### Scenario: Bloqueio de campos sensíveis
- **WHEN** uma solicitação está selecionada no painel direito
- **THEN** o CPF do tutor e as respostas do questionário de triagem MUST permanecer estritamente bloqueados para edição (modo somente leitura).

#### Scenario: Edição controlada de contatos via modal
- **WHEN** o usuário clica no botão "Editar Contatos" de uma solicitação selecionada
- **THEN** o sistema MUST abrir um modal permitindo alterar exclusivamente telefone, e-mail e endereço do tutor
- **AND** ao confirmar, MUST enviar a atualização (`PATCH`) autenticada ao Xano e refletir os novos dados na interface somente após confirmação do backend, exibindo feedback via *toast*.

### Requirement: Atualização de Status do Processo de Adoção

O sistema MUST permitir que o administrador atualize o status do processo de adoção (`Em análise`, `Aprovada`, `Adoção efetivada`, `Recusada`) diretamente no painel de detalhes.

#### Scenario: Alteração válida do status da adoção
- **WHEN** o administrador seleciona um novo status e confirma a atualização
- **THEN** o sistema MUST enviar uma requisição `PATCH` autenticada ao endpoint de `PROCESSO_ADOCAO` no Xano
- **AND** MUST atualizar o badge de status na lista Master e no painel Detail, exibindo confirmação via *toast*.

#### Scenario: Falha ao atualizar status ou contatos
- **WHEN** o backend Xano rejeitar a alteração ou ocorrer falha de rede
- **THEN** o sistema MUST preservar os dados anteriores na interface e exibir mensagem de erro via *toast*.
