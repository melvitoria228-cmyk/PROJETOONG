# Proposta: Atendimento Veterinário

## Why

Os atendimentos veterinários precisam ter seus registros organizados para facilitar a consulta dos cuidados médicos recebidos pelos animais e o acompanhamento de sua condição de saúde.

## What Changes

Será implementada a tela administrativa de Atendimento Veterinário, seguindo o layout de Agenda Clínica com Histórico Breve definido na UI/UX V5.

A tela contemplará:

- Agenda clínica com navegação por dias e semanas.
- Visualização dos atendimentos em uma grade de horários.
- Ação para novo agendamento.
- Ficha resumida do animal selecionado.
- Destaque para alertas clínicos e restrições.
- Exibição dos três atendimentos realizados mais recentes.
- Acesso ao histórico veterinário completo.
- Formulário para registrar agendamentos e atendimentos veterinários.

Os registros utilizarão os campos existentes na entidade `ATENDIMENTO_VETERINARIO`:

- `id`
- `animal_id`
- `data_atendimento`
- `horario_atendimento`
- `diagnostico`
- `procedimentos`
- `tratamento`
- `custo`
- `veterinario_responsavel`
- `peso`
- `status_atendimento`

A ficha clínica utilizará os dados disponíveis na entidade `ANIMAL`, incluindo nome, espécie, raça, idade estimada, sexo, condição de saúde, alergias, restrições clínicas e fotografia.

## Impact

- Área administrativa do sistema.
- Entidades `ANIMAL` e `ATENDIMENTO_VETERINARIO`.
- Consulta e registro dos atendimentos veterinários.
- Organização dos agendamentos e do histórico clínico dos animais.

## Considerations

Os agendamentos e atendimentos realizados serão diferenciados pelo campo `status_atendimento`.

Os dados clínicos, como diagnóstico, procedimentos, tratamento, custo e peso, poderão permanecer vazios enquanto o atendimento estiver apenas agendado.

