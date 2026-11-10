# Spec: Módulo de Adoções

## ADDED Requirements

### Requirement: Estrutura Master-Detail (Split View)
The system MUST display a 35/65 split view layout for managing adoptions.

#### Scenario: Filtragem e Seleção na Lista Master
- GIVEN que o utilizador está na página do Módulo de Adoções
- WHEN introduz texto na barra de pesquisa ou altera o filtro de status
- THEN a lista master da coluna esquerda DEVE atualizar dinamicamente para exibir apenas as solicitações correspondentes.

#### Scenario: Seleção de um Item da Lista
- GIVEN que a lista master exibe as solicitações filtradas
- WHEN o utilizador clica num card da coluna esquerda
- THEN a coluna direita DEVE carregar imediatamente os detalhes completos da solicitação selecionada.

### Requirement: Imutabilidade e Auditabilidade de Dados
The system MUST enforce read-only restrictions on sensitive fields to preserve auditability.

#### Scenario: Bloqueio de Campos Sensíveis
- GIVEN que uma solicitação está selecionada no painel direito
- WHEN o utilizador inspeciona os campos do CPF do tutor ou as respostas do questionário de compatibilidade
- THEN estes campos DEVEM permanecer estritamente em modo de leitura.

#### Scenario: Edição Controlada de Contatos via Modal
- GIVEN que uma solicitação está selecionada
- WHEN o utilizador clica no botão "Editar Contatos"
- THEN uma janela modal DEVE ser exibida permitindo alterar APENAS o telefone, e-mail e endereço.
- AND ao salvar, as alterações DEVEM refletir imediatamente no estado global da aplicação.
