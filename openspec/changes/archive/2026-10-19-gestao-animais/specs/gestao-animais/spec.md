## Purpose

Definir os requisitos funcionais da tela administrativa de Gestão de Animais (`/animais`), permitindo que a equipe da ONG consulte, filtre, visualize e mantenha os registros dos animais resgatados de forma organizada e integrada aos dados armazenados no Xano.

## ADDED Requirements

### Requirement: Consultar animais cadastrados e indicadores resumidos

O sistema MUST permitir que usuários administrativos consultem os animais cadastrados na rota `/animais`, apresentando os indicadores resumidos (KPIs), a listagem paginada e o status atual de cada registro.

#### Scenario: Existem animais cadastrados

- **WHEN** o usuário administrativo acessar a rota `/animais` e houver registros cadastrados no Xano
- **THEN** o sistema MUST disparar a consulta autenticada automaticamente (`on_load`), exibir os cartões de resumo (total de cadastros, cães, gatos e resgates nos últimos 30 dias) e apresentar a tabela paginada com código, miniatura/avatar, nome, espécie, sexo, raça, porte, idade estimada, data de resgate, condição de saúde e status atual.

#### Scenario: Não existem animais cadastrados

- **WHEN** o usuário administrativo acessar a rota `/animais` e não houver registros
- **THEN** o sistema MUST informar que não existem animais cadastrados.

#### Scenario: Falha ao consultar os animais

- **WHEN** o sistema não conseguir obter os registros no Xano
- **THEN** o sistema MUST informar que ocorreu um erro ao carregar os animais via notificação *toast*.

### Requirement: Buscar e filtrar animais na listagem

O sistema MUST permitir refinar a listagem de animais por meio de busca textual e filtros combinados sem alterar os dados persistidos no backend.

#### Scenario: Filtragem por busca textual e atributos

- **WHEN** o administrador digitar um termo na busca (nome ou código) ou selecionar filtros de espécie, porte ou status
- **THEN** o sistema MUST atualizar dinamicamente os registros exibidos na tabela conforme os critérios selecionados.

#### Scenario: Limpar filtros aplicados

- **WHEN** o administrador limpar os campos de busca e filtros
- **THEN** o sistema MUST restaurar a exibição completa dos registros carregados.

### Requirement: Cadastrar animais resgatados

O sistema MUST permitir que o usuário administrativo cadastre animais que já foram resgatados, utilizando os campos definidos para a entidade `ANIMAL`.

Os campos de negócio são `nome`, `especie`, `raca`, `idade_estimada`, `sexo`, `porte`, `condicao_saude`, `status_atual`, `data_resgate` e `foto_url` (opcional).

#### Scenario: Cadastro válido

- **WHEN** o usuário preencher todos os campos obrigatórios com informações válidas e confirmar o cadastro
- **THEN** o sistema MUST enviar os dados autenticados ao endpoint `POST` no Xano e exibir a confirmação via *toast*
- **AND** o sistema MUST atualizar a listagem e os indicadores somente após confirmar o sucesso do cadastro.

#### Scenario: Cadastro com informações obrigatórias ausentes

- **WHEN** o usuário tentar cadastrar um animal sem preencher um campo obrigatório
- **THEN** o sistema MUST impedir o envio e indicar os campos que precisam ser preenchidos.

#### Scenario: Falha ao cadastrar

- **WHEN** o Xano não conseguir registrar o animal ou ocorrer uma falha de comunicação
- **THEN** o sistema MUST informar que o cadastro não foi concluído
- **AND** o sistema MUST NOT apresentar o cadastro como bem-sucedido nem adicionar um registro não confirmado à lista.

### Requirement: Padronizar as opções dos campos

O sistema MUST utilizar opções padronizadas nos campos `especie`, `sexo`, `porte` e `status_atual`, mantendo compatibilidade com os valores aceitos e armazenados no Xano.

As opções previstas são:

- `especie`: Cão, Gato e Outros.
- `sexo`: Macho, Fêmea e Não identificado.
- `porte`: Mini, Pequeno, Médio e Grande.
- `status_atual`: Disponível, Em Lar Temporário, Em Processo de Adoção, Adotado e Falecido.

#### Scenario: Selecionar uma opção padronizada

- **WHEN** o usuário preencher um dos campos que possuem opções padronizadas
- **THEN** o sistema MUST apresentar as opções definidas para esse campo e enviar ao Xano o valor correspondente à opção selecionada.

#### Scenario: Exibir um valor já armazenado

- **WHEN** o sistema apresentar um animal cujo campo contenha um valor já armazenado no Xano
- **THEN** o sistema MUST preservar e apresentar o valor correspondente ao registro, tratando valores inesperados sem causar falha na tela.

### Requirement: Visualizar detalhes e ampliar fotografia do animal

O sistema MUST permitir que o usuário administrativo consulte os detalhes completos de um animal cadastrado e visualize sua fotografia (`foto_url`) em tamanho ampliado.

#### Scenario: Consultar detalhes de um animal existente

- **WHEN** o usuário selecionar a ação de visualização de um animal cadastrado
- **THEN** o sistema MUST exibir um modal com todos os dados disponíveis daquele registro.

#### Scenario: Ampliar foto do animal

- **WHEN** o usuário clicar na miniatura da foto de um animal que possua `foto_url` preenchida
- **THEN** o sistema MUST abrir um modal exibindo a fotografia em tamanho ampliado.

#### Scenario: Animal sem URL de foto cadastrada

- **WHEN** um registro de animal não possuir `foto_url` ou a URL estiver indisponível
- **THEN** o sistema MUST exibir um avatar neutro padronizado com ícone institucional, sem quebrar o layout da tabela.

### Requirement: Editar animais cadastrados

O sistema MUST permitir que o usuário administrativo altere os dados de um animal cadastrado, respeitando os campos obrigatórios e as restrições existentes no Xano.

#### Scenario: Edição válida

- **WHEN** o usuário alterar os dados de um animal e confirmar a edição
- **THEN** o sistema MUST enviar as alterações ao endpoint `PATCH` correspondente no Xano
- **AND** o sistema MUST atualizar a listagem e os indicadores somente após confirmar o sucesso da operação.

#### Scenario: Falha ao editar

- **WHEN** o Xano não conseguir salvar as alterações ou ocorrer uma falha de comunicação
- **THEN** o sistema MUST informar que a edição não foi concluída
- **AND** o sistema MUST NOT apresentar as alterações como salvas sem confirmação do backend.

### Requirement: Excluir animais cadastrados

O sistema MUST permitir que o usuário administrativo solicite a exclusão de um animal, respeitando as regras de negócio e os relacionamentos existentes.

#### Scenario: Exclusão permitida

- **WHEN** o usuário solicitar a exclusão de um animal
- **THEN** o sistema MUST solicitar confirmação por meio de modal antes de enviar a operação
- **AND** o sistema MUST informar o resultado da exclusão via *toast*
- **AND** o sistema MUST remover o registro da lista somente após confirmar o sucesso no Xano (`DELETE`).

#### Scenario: Exclusão cancelada

- **WHEN** o usuário cancelar a confirmação de exclusão
- **THEN** o sistema MUST manter o registro sem enviar a solicitação de exclusão ao Xano.

#### Scenario: Exclusão impedida

- **WHEN** a exclusão não for permitida devido a regras de negócio, relacionamentos ativos (`PROCESSO_ADOCAO`, `ATENDIMENTO_VETERINARIO` ou `ANIMAL_LAR_TEMPORARIO`) ou falha no Xano
- **THEN** o sistema MUST manter o registro na lista e informar que não foi possível excluí-lo.

### Requirement: Integrar a tela aos dados do Xano

O sistema MUST utilizar os endpoints existentes da tabela `ANIMAL` no grupo de API `PortoSeguroPet` para realizar as operações de consulta, cadastro, edição e exclusão, autenticando as requisições com o token JWT da sessão (`LoginState.token`).

A URL da API de animais MUST ser carregada a partir de variável de ambiente (`XANO_ANIMAL_URL`), mantendo configurações sensíveis fora do código-fonte.

#### Scenario: Operação concluída

- **WHEN** uma operação sobre os animais for concluída com sucesso no Xano
- **THEN** o sistema MUST apresentar o resultado confirmado da operação na interface.

#### Scenario: Falha de comunicação com o Xano

- **WHEN** ocorrer uma falha de comunicação ou o backend rejeitar uma operação
- **THEN** o sistema MUST informar que a operação não foi concluída
- **AND** o sistema MUST preservar na interface os dados confirmados anteriormente, sem apresentar sucesso indevidamente.