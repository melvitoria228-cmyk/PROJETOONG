# Design: Atendimento Veterinário

## Context

O módulo de Atendimento Veterinário pertence à área administrativa do Porto Seguro Pet e tem como objetivo organizar os agendamentos e os registros dos cuidados médicos dos animais.

## Goals

- Organizar os agendamentos veterinários.
- Facilitar a consulta do histórico clínico.
- Registrar os atendimentos realizados.
- Destacar alergias e restrições clínicas.

## Decisions

### Organização da Interface

A tela será dividida em duas áreas:

- **Agenda Clínica:** exibição dos agendamentos por dias e horários, com opção para cadastrar novos registros.
- **Histórico e Ficha Clínica:** apresentação das informações do animal selecionado, dos atendimentos recentes e dos alertas clínicos.

### Agendamentos e Atendimentos

Os registros serão armazenados na entidade `ATENDIMENTO_VETERINARIO`, utilizando os campos:

`id`, `animal_id`, `data_atendimento`, `horario_atendimento`, `diagnostico`, `procedimentos`, `tratamento`, `custo`, `veterinario_responsavel`, `peso` e `status_atendimento`.

O campo `status_atendimento` diferenciará os registros entre `Agendado`, `Realizado` e `Cancelado`.

Os dados clínicos poderão ser preenchidos após a realização do atendimento.

Na agenda, as cores identificarão o tipo de procedimento:

- Verde: vacinação.
- Vermelho: cirurgia.
- Amarelo: consulta.

O status será apresentado separadamente.

### Ficha Clínica e Histórico

A ficha apresentará os dados disponíveis do animal, incluindo fotografia, nome, espécie, raça, idade estimada, sexo, condição de saúde, alergias e restrições clínicas.

Também serão exibidos os três atendimentos realizados mais recentes, com acesso ao histórico completo.

O peso será registrado nos atendimentos realizados, permitindo consultar seu histórico.

## Constraints

- Cada atendimento deverá estar relacionado a um animal.
- Um animal poderá possuir vários registros veterinários.
- Os registros realizados deverão ser preservados para consulta.
- Alergias e restrições clínicas serão obtidas do cadastro do animal.
- A implementação deverá respeitar os campos definidos no Xano.