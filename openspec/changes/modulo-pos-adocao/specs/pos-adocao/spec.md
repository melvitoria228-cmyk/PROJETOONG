# Spec: Módulo de Pós-Adoção (Timeline de Acompanhamento)

## ADDED Requirements

### Requirement: Exibição da Linha do Tempo e Acompanhamento de Animais Adotados

O sistema SHALL exibir os processos de adoção efetivados e permitir a consulta e o registro de acompanhamentos vinculados a esses processos.

#### Scenario: Exibição da lista de animais adotados

- **Given** que o usuário administrador está autenticado na área administrativa
- **When** ele acessa a rota `/pos-adocao`
- **Then** o sistema SHALL exibir os processos de adoção cujo `status_processo` seja `Adoção efetivada`, apresentando as informações dos respectivos animais e tutores.

#### Scenario: Visualização do histórico de acompanhamento

- **Given** que o administrador selecionou um animal na lista de adoções efetivadas
- **When** o sistema consulta os registros de acompanhamento vinculados ao processo de adoção correspondente
- **Then** o sistema SHALL exibir os registros em ordem cronológica decrescente, utilizando o campo `data_acompanhamento`, apresentando a data e o relatório de observação de cada registro.

#### Scenario: Registro de novo acompanhamento pós-adoção

- **Given** que o administrador selecionou um animal na tela de pós-adoção
- **When** ele aciona a opção de adicionar novo registro e informa a data e o relatório de observação
- **Then** o sistema SHALL registrar o acompanhamento na tabela `ACOMPANHAMENTO_POS_ADOCAO`, vinculando-o ao processo de adoção selecionado por meio do campo `processo_adocao_id`.

#### Scenario: Consulta de animal sem registros de acompanhamento

- **Given** que o administrador selecionou um animal cuja adoção foi efetivada
- **When** não existem registros de acompanhamento vinculados ao processo de adoção
- **Then** o sistema SHALL apresentar uma mensagem informando que ainda não existem registros de acompanhamento para aquele animal.
