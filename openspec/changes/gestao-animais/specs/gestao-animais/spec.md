## Purpose

Definir os requisitos funcionais da tela administrativa de Gestão de Animais, permitindo que a equipe da ONG consulte e mantenha os registros dos animais resgatados de forma organizada e integrada aos dados armazenados no Xano.

## ADDED Requirements

### Requirement: Consultar animais cadastrados

O sistema MUST permitir que usuários administrativos consultem os animais cadastrados no sistema, apresentando as informações disponíveis de cada registro.

#### Scenario: Existem animais cadastrados

- **WHEN** o usuário administrativo acessar a tela de Gestão de Animais e houver registros cadastrados
- **THEN** o sistema MUST apresentar os animais e suas informações disponíveis, incluindo o status atual.

#### Scenario: Não existem animais cadastrados

- **WHEN** o usuário administrativo acessar a tela de Gestão de Animais e não houver registros
- **THEN** o sistema MUST informar que não existem animais cadastrados.

#### Scenario: Falha ao consultar os animais

- **WHEN** o sistema não conseguir obter os registros no Xano
- **THEN** o sistema MUST informar que ocorreu um erro ao carregar os animais.

### Requirement: Cadastrar animais resgatados

O sistema MUST permitir que o usuário administrativo cadastre animais que já foram resgatados, utilizando os campos definidos para a entidade ANIMAL.

Os campos de negócio são nome, especie, raca, idade_estimada, sexo, porte, condicao_saude, status_atual e data_resgate.

#### Scenario: Cadastro válido

- **WHEN** o usuário preencher todos os campos obrigatórios com informações válidas e confirmar o cadastro
- **THEN** o sistema MUST enviar os dados ao Xano e informar o resultado da operação
- **AND** o sistema MUST atualizar a lista somente após confirmar o sucesso do cadastro.

#### Scenario: Cadastro com informações obrigatórias ausentes

- **WHEN** o usuário tentar cadastrar um animal sem preencher um campo obrigatório
- **THEN** o sistema MUST impedir o envio e indicar os campos que precisam ser preenchidos.

#### Scenario: Falha ao cadastrar

- **WHEN** o Xano não conseguir registrar o animal ou ocorrer uma falha de comunicação
- **THEN** o sistema MUST informar que o cadastro não foi concluído
- **AND** o sistema MUST NOT apresentar o cadastro como bem-sucedido nem adicionar um registro não confirmado à lista.

### Requirement: Padronizar as opções dos campos

O sistema MUST utilizar opções padronizadas nos campos especie, sexo, porte e status_atual, mantendo compatibilidade com os valores aceitos e armazenados no Xano.

As opções previstas são:

- especie: Cão, Gato e Outros.
- sexo: Macho, Fêmea e Não identificado.
- porte: Mini, Pequeno, Médio e Grande.
- status_atual: Disponível, Em Lar Temporário, Em Processo de Adoção, Adotado e Falecido.

Antes da implementação, os valores já armazenados no Xano deverão ser conferidos para evitar divergências de escrita e acentuação.

#### Scenario: Selecionar uma opção padronizada

- **WHEN** o usuário preencher um dos campos que possuem opções padronizadas
- **THEN** o sistema MUST apresentar as opções definidas para esse campo e enviar ao Xano o valor correspondente à opção selecionada.

#### Scenario: Exibir um valor já armazenado

- **WHEN** o sistema apresentar um animal cujo campo contenha um valor já armazenado no Xano
- **THEN** o sistema MUST preservar e apresentar o valor correspondente ao registro, tratando valores inesperados sem causar falha na tela.

### Requirement: Visualizar detalhes de um animal

O sistema MUST permitir que o usuário administrativo consulte os detalhes de um animal cadastrado.

#### Scenario: Consultar um animal existente

- **WHEN** o usuário selecionar um animal cadastrado
- **THEN** o sistema MUST apresentar os dados disponíveis daquele animal, correspondentes ao registro selecionado.

### Requirement: Editar animais cadastrados

O sistema MUST permitir que o usuário administrativo altere os dados de um animal cadastrado, respeitando os campos obrigatórios e as restrições existentes no Xano.

#### Scenario: Edição válida

- **WHEN** o usuário alterar os dados de um animal e confirmar a edição
- **THEN** o sistema MUST enviar as alterações ao endpoint correto do Xano
- **AND** o sistema MUST atualizar a lista somente após confirmar o sucesso da operação.

#### Scenario: Falha ao editar

- **WHEN** o Xano não conseguir salvar as alterações ou ocorrer uma falha de comunicação
- **THEN** o sistema MUST informar que a edição não foi concluída
- **AND** o sistema MUST NOT apresentar as alterações como salvas sem confirmação do backend.

### Requirement: Excluir animais cadastrados

O sistema MUST permitir que o usuário administrativo solicite a exclusão de um animal, respeitando as regras de negócio e os relacionamentos existentes.

#### Scenario: Exclusão permitida

- **WHEN** o usuário solicitar a exclusão de um animal
- **THEN** o sistema MUST solicitar confirmação antes de enviar a operação
- **AND** o sistema MUST informar o resultado da exclusão
- **AND** o sistema MUST remover o registro da lista somente após confirmar o sucesso no Xano.

#### Scenario: Exclusão cancelada

- **WHEN** o usuário cancelar a confirmação de exclusão
- **THEN** o sistema MUST manter o registro sem enviar a solicitação de exclusão ao Xano.

#### Scenario: Exclusão impedida

- **WHEN** a exclusão não for permitida devido a regras de negócio, relacionamentos ou falha no Xano
- **THEN** o sistema MUST manter o registro na lista e informar que não foi possível excluí-lo.

### Requirement: Integrar a tela aos dados do Xano

O sistema MUST utilizar os endpoints existentes da tabela ANIMAL no grupo de API PortoSeguroPet para realizar as operações de consulta, cadastro, edição e exclusão, sem duplicar endpoints ou criar tabelas nesta mudança.

A integração MUST respeitar os tipos, os campos obrigatórios e os relacionamentos existentes no backend. A configuração da URL da API de animais deverá permanecer fora do código-fonte, reutilizando o mecanismo de configuração por ambiente do projeto.

#### Scenario: Operação concluída

- **WHEN** uma operação sobre os animais for concluída com sucesso no Xano
- **THEN** o sistema MUST apresentar o resultado confirmado da operação na interface.

#### Scenario: Falha de comunicação com o Xano

- **WHEN** ocorrer uma falha de comunicação ou o backend rejeitar uma operação
- **THEN** o sistema MUST informar que a operação não foi concluída
- **AND** o sistema MUST preservar na interface os dados confirmados anteriormente, sem apresentar sucesso indevidamente.
