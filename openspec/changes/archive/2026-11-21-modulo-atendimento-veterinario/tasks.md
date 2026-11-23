# Tasks: Atendimento Veterinário

## 1. Estrutura Modular e Interface Base (`ProjetoONG/atendimento_vet.py`)

- [x] 1.1 Criar o arquivo `ProjetoONG/atendimento_vet.py` com a página `pagina_atendimento_vet` integrada ao menu lateral fixo `sidebar_administracao()`.
- [x] 1.2 Organizar a tela em duas áreas principais: **Agenda Clínica** à esquerda e **Ficha Clínica Resumida e Histórico** à direita.
- [x] 1.3 Aplicar a paleta institucional da Área Administrativa (Areia `#EFE6DA`, Bege Claro `#F8F3EC`, Terracota `#A96348` e Verde Oliva `#737747`) mantendo os acentos semânticos clínicos.

## 2. Agenda Clínica e Agendamentos (`ProjetoONG/atendimento_vet_state.py` e `atendimento_vet.py`)

- [x] 2.1 Implementar a grade de agendamentos organizada por data e horário em `AtendimentoVetState`.
- [x] 2.2 Implementar os controles de navegação entre dias/semanas e o filtro por status (`Agendado`, `Realizado`, `Cancelado`).
- [x] 2.3 Diferenciar visualmente os tipos de procedimento por cor (verde para vacinação, vermelho para cirurgia, amarelo/âmbar para consulta) separados do badge de status.
- [x] 2.4 Implementar o modal e a ação de cadastro de novo agendamento (`POST` no Xano) vinculado ao animal selecionado com status inicial `Agendado`.

## 3. Ficha Clínica Resumida e Histórico Médico

- [x] 3.1 Implementar a seleção de animal pela agenda ou seletor clínico no `AtendimentoVetState`.
- [x] 3.2 Exibir a fotografia (`foto_url` com fallback seguro) e os dados cadastrais do animal selecionado (nome, espécie, raça, idade estimada, sexo e condição de saúde).
- [x] 3.3 Destacar visualmente alergias e restrições clínicas cadastradas na entidade `ANIMAL` em faixa de alerta.
- [x] 3.4 Exibir os três atendimentos realizados mais recentes e o histórico de peso registrado nas consultas concluídas.
- [x] 3.5 Implementar a consulta do histórico veterinário completo do animal selecionado em modo de leitura preservando registros anteriores.

## 4. Registro e Conclusão de Atendimentos Clínicos

- [x] 4.1 Implementar o modal e o formulário de registro/conclusão de atendimento veterinário (`PATCH` / `POST` no Xano).
- [x] 4.2 Permitir o preenchimento dos dados clínicos pós-consulta (diagnóstico, procedimentos, tratamento, custo, veterinário responsável e peso).
- [x] 4.3 Implementar a atualização de `status_atendimento` para `Realizado` ou `Cancelado` com sincronização imediata da agenda e feedback via `rx.toast`.

## 5. Integração com Xano, Roteamento e Validação (`ProjetoONG/ProjetoONG.py`)

- [x] 5.1 Integrar `AtendimentoVetState` aos endpoints autenticados do Xano (`ATENDIMENTO_VETERINARIO` e `ANIMAL`) via `httpx` com token JWT (`LoginState.token`).
- [x] 5.2 Registrar a rota `/atendimento-vet` em `ProjetoONG/ProjetoONG.py` com carregamento automático no ciclo `on_load`.
- [x] 5.3 Testar o cadastro de agendamentos, a conclusão clínica, a consulta de histórico/alertas e validar a compilação sem erros (`openspec validate`).