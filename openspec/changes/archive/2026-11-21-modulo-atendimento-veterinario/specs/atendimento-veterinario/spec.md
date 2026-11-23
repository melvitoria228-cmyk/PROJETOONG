# Spec: Atendimento Veterinário

## Purpose

Definir os requisitos funcionais do módulo administrativo de **Atendimento Veterinário** na rota `/atendimento-vet`, permitindo gerenciar a agenda clínica, visualizar alertas médicos e o histórico recente de cada animal resgatado e registrar novos agendamentos ou atendimentos concluídos integrados ao backend Xano.

## ADDED Requirements

### Requirement: Agenda Clínica e Carregamento Automático

O sistema SHALL carregar automaticamente os registros veterinários e dados dos animais no `on_load` da rota `/atendimento-vet` (via token JWT do Xano) e apresentar uma agenda para organizar os agendamentos por data e horário.

#### Scenario: Visualizar agenda clínica

- **WHEN** o administrador acessar a rota `/atendimento-vet`
- **THEN** o sistema SHALL carregar os registros autenticados do Xano e apresentar os agendamentos em uma grade de horários
- **AND** SHALL permitir a navegação entre dias e semanas e a filtragem por status (`Agendado`, `Realizado`, `Cancelado`).

#### Scenario: Identificar tipo de procedimento e status

- **WHEN** os agendamentos forem exibidos na agenda
- **THEN** o sistema SHALL identificar visualmente o tipo de procedimento por cor (verde para vacinação, vermelho para cirurgia e amarelo/âmbar para consulta)
- **AND** SHALL apresentar separadamente o badge de status do atendimento.

#### Scenario: Falha de comunicação com o backend

- **WHEN** ocorrer falha na consulta ou gravação junto ao Xano
- **THEN** o sistema SHALL preservar o estado atual da interface e notificar o usuário via *toast*.

### Requirement: Cadastro de Agendamentos e Registro de Atendimentos

O sistema SHALL permitir cadastrar novos agendamentos (`POST`) e registrar ou concluir atendimentos veterinários (`PATCH` / `POST`) integrados ao Xano.

#### Scenario: Cadastrar novo agendamento

- **WHEN** o administrador abrir o formulário de novo agendamento e informar o animal, a data, o horário, o tipo de procedimento e o veterinário responsável
- **THEN** o sistema SHALL enviar o registro autenticado ao Xano com `status_atendimento` definido como `Agendado` (permitindo campos clínicos pós-consulta vazios)
- **AND** SHALL atualizar a agenda imediatamente com feedback via *toast*.

#### Scenario: Registrar atendimento realizado

- **WHEN** um atendimento agendado for concluído pelo administrador
- **THEN** o sistema SHALL permitir registrar o diagnóstico, os procedimentos, o tratamento, o custo e o peso do animal
- **AND** SHALL atualizar o status para `Realizado` no Xano, refletindo o registro no histórico clínico do pet.

#### Scenario: Cancelar agendamento

- **WHEN** um agendamento for cancelado pelo administrador
- **THEN** o sistema SHALL atualizar seu `status_atendimento` para `Cancelado` no Xano e refletir a alteração na agenda.

### Requirement: Consulta do Histórico Veterinário

O sistema SHALL permitir consultar os registros veterinários realizados relacionados a cada animal selecionado.

#### Scenario: Visualizar atendimentos recentes

- **WHEN** o administrador selecionar um animal na agenda ou no seletor clínico
- **THEN** o sistema SHALL apresentar os três atendimentos realizados mais recentes, quando disponíveis.

#### Scenario: Consultar histórico completo

- **WHEN** o administrador solicitar a visualização do histórico completo do animal selecionado
- **THEN** o sistema SHALL exibir todos os registros veterinários realizados para aquele animal em ordem cronológica.

#### Scenario: Preservar registros anteriores realizados

- **WHEN** o administrador consultar um atendimento já concluído (`Realizado`)
- **THEN** o sistema SHALL exibir suas informações clínicas em modo de consulta sem permitir a exclusão ou adulteração do histórico médico.

### Requirement: Ficha Clínica Resumida do Animal

O sistema SHALL apresentar as informações cadastrais e alertas médicos do animal selecionado para apoiar a avaliação clínica.

#### Scenario: Visualizar informações clínicas e fotografia

- **WHEN** o administrador selecionar um animal
- **THEN** o sistema SHALL apresentar sua fotografia (`foto_url` com fallback seguro) e seus dados clínicos disponíveis: nome, espécie, raça, idade estimada, sexo e condição de saúde.

#### Scenario: Destacar alertas clínicos

- **WHEN** o animal possuir alergias ou restrições clínicas cadastradas na entidade `ANIMAL`
- **THEN** o sistema SHALL destacar essas informações visualmente em faixa de alerta na ficha clínica.

#### Scenario: Consultar evolução de peso

- **WHEN** existirem registros de atendimentos realizados com peso informado
- **THEN** o sistema SHALL permitir consultar o peso registrado ao longo dos atendimentos do animal.