# Proposal: Atendimento Veterinário

## Why

A equipe administrativa do **Porto Seguro Pet** precisa organizar os agendamentos e os registros clínicos dos animais resgatados de forma centralizada, rápida e segura na rota `/atendimento-vet`.

Sem uma agenda clínica integrada ao prontuário resumido de cada animal, torna-se difícil acompanhar consultas agendadas, visualizar alertas de alergias ou restrições antes de um procedimento e consultar o histórico médico recente de cada pet. Era necessário estruturar uma interface clínica conectada diretamente ao backend **Xano** que unisse a agenda diária/semanal à ficha clínica resumida do animal selecionado.

## What Changes

- Implementar o módulo administrativo de **Atendimento Veterinário** na rota `/atendimento-vet`, integrado ao menu lateral fixo (`sidebar_administracao`) em `ProjetoONG.py` com carregamento automático no `on_load`.
- Estruturar a interface no formato de **Agenda Clínica com Histórico Breve**:
  - **Agenda Clínica:** navegação por dias/período, visualização dos agendamentos e atendimentos organizados por data e horário, filtro por status (`Agendado`, `Realizado`, `Cancelado`) e ação rápida para **Novo Agendamento**.
  - **Ficha Clínica Resumida do Animal Selecionado:** exibição dos dados essenciais do pet (`nome`, `espécie`, `raça`, `idade_estimada`, `sexo` e fotografia), destaque visual para alertas clínicos (`condicao_saude`, `alergias` e `restricoes_clinicas`), listagem dos **3 atendimentos realizados mais recentes** e acesso ao histórico veterinário completo.
- Implementar modais para **Agendamento de Consulta** (`POST`) e **Registro/Conclusão de Atendimento Clínico** (`PATCH` / `POST`), utilizando os atributos da entidade `ATENDIMENTO_VETERINARIO`:
  - `id`, `animal_id`, `data_atendimento`, `horario_atendimento`, `diagnostico`, `procedimentos`, `tratamento`, `custo`, `veterinario_responsavel`, `peso` e `status_atendimento`.
- Integrar todas as operações de consulta, criação e atualização aos endpoints autenticados do **Xano** via requisições assíncronas (`httpx`) com token JWT (`LoginState.token`) e feedback via `rx.toast`.

## Capabilities

### New Capabilities

- `atendimento-veterinario`: agenda clínica interativa na rota `/atendimento-vet`, ficha clínica resumida com alertas médicos do animal, visualização dos 3 atendimentos mais recentes, histórico completo e formulários de agendamento/registro clínico integrados ao Xano.

### Modified Capabilities

Nenhuma.

## Impact

- **Frontend Reflex (`ProjetoONG/atendimento_vet_state.py` e `ProjetoONG/atendimento_vet.py`):** criação do estado `AtendimentoVetState` e da página `pagina_atendimento_vet` seguindo a paleta institucional da Área Administrativa.
- **Arquivo Principal (`ProjetoONG/ProjetoONG.py`):** registro da rota `/atendimento-vet` com disparo automático de carregamento no `on_load` e vinculação ao menu lateral `sidebar_administracao()`.
- **Backend Xano:** consumo autenticado das entidades `ATENDIMENTO_VETERINARIO` e `ANIMAL` (`GET`, `POST` e `PATCH`), diferenciando agendamentos pendentes de atendimentos concluídos através do campo `status_atendimento` (permitindo campos clínicos vazios enquanto apenas agendado).