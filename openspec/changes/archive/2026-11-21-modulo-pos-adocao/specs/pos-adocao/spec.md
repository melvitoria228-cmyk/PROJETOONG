# Spec: Módulo de Pós-Adoção

## Purpose

Definir os requisitos funcionais do módulo administrativo de **Pós-Adoção** na rota `/pos-adocao`, permitindo consultar exclusivamente processos com status `Adoção efetivada`, pesquisar animais e tutores adotantes, visualizar o histórico cronológico decrescente em **Linha do Tempo (Timeline)** e registrar novos acompanhamentos integrados ao backend Xano.

## ADDED Requirements

### Requirement: Exibição e Filtragem da Lista de Animais Adotados

O sistema SHALL carregar automaticamente no `on_load` da rota `/pos-adocao` (via token JWT do Xano) os processos de adoção com status `Adoção efetivada` e exibi-los na coluna de seleção (~30%) com suporte a pesquisa.

#### Scenario: Exibição da lista de animais adotados

- **WHEN** o administrador autenticado acessar a rota `/pos-adocao`
- **THEN** o sistema SHALL consultar os registros no Xano e exibir exclusivamente os processos de adoção cujo `status_processo` seja `Adoção efetivada`
- **AND** SHALL apresentar em cada cartão a fotografia em miniatura (com fallback seguro), o nome do animal e os dados de identificação/contato do respectivo tutor.

#### Scenario: Filtragem da lista de adoções efetivadas

- **WHEN** o administrador digitar um termo no campo de pesquisa por nome do animal ou do tutor
- **THEN** o sistema SHALL filtrar em tempo real a coluna de seleção exibindo apenas os processos correspondentes.

#### Scenario: Falha de comunicação com o backend

- **WHEN** ocorrer erro de rede ou rejeição na consulta ou gravação junto ao Xano
- **THEN** o sistema SHALL preservar o estado atual da interface e notificar o usuário via *toast*.

### Requirement: Linha do Tempo (Timeline) e Registro de Acompanhamentos Pós-Adoção

O sistema SHALL apresentar na área principal (~70%) os dados do animal e tutor selecionados, exibir o histórico de acompanhamentos em ordem cronológica decrescente e permitir a inclusão de novos registros em `ACOMPANHAMENTO_POS_ADOCAO`.

#### Scenario: Visualização do histórico de acompanhamento em ordem decrescente

- **WHEN** o administrador selecionar um animal na lista de adoções efetivadas
- **THEN** o sistema SHALL exibir no cabeçalho os dados do animal, contato e endereço do tutor (quando disponível)
- **AND** SHALL apresentar na Linha do Tempo os registros de `ACOMPANHAMENTO_POS_ADOCAO` vinculados ao processo em ordem cronológica decrescente (do mais recente para o mais antigo), exibindo `data_acompanhamento` e `relatorio_observacao`.

#### Scenario: Consulta de animal sem registros de acompanhamento

- **WHEN** o administrador selecionar um animal cuja adoção foi efetivada e ainda não existirem registros vinculados ao processo
- **THEN** o sistema SHALL apresentar uma mensagem informativa indicando que ainda não há registros de acompanhamento para aquele animal.

#### Scenario: Registro de novo acompanhamento pós-adoção

- **WHEN** o administrador acionar a opção de adicionar novo registro e informar a data (`data_acompanhamento`) e o relatório de observação (`relatorio_observacao`)
- **THEN** o sistema SHALL enviar o registro autenticado (`POST`) para a tabela `ACOMPANHAMENTO_POS_ADOCAO` vinculado ao `processo_adocao_id` selecionado
- **AND** SHALL atualizar imediatamente a Linha do Tempo com feedback via *toast*.