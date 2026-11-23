# Design: Atendimento Veterinário

## Context

O módulo de **Atendimento Veterinário** integra a Área Administrativa do **Porto Seguro Pet** (rota `/atendimento-vet`) e tem como objetivo organizar os agendamentos clínicos, centralizar o prontuário resumido de cada animal resgatado e registrar os cuidados médicos realizados pela equipe.

A interface comunica-se de forma assíncrona e autenticada via JWT com as entidades `ATENDIMENTO_VETERINARIO` e `ANIMAL` no backend **Xano**, compartilhando a navegação lateral unificada `sidebar_administracao()` em `ProjetoONG.py`.

## Goals / Non-Goals

**Goals:**
- Organizar os agendamentos e atendimentos veterinários em uma **Agenda Clínica** navegável por datas e horários na rota `/atendimento-vet` com carregamento automático (`on_load`).
- Facilitar a consulta rápida do histórico clínico do animal selecionado (exibindo os **3 atendimentos realizados mais recentes** e acesso ao histórico completo).
- Destacar visualmente alergias, restrições clínicas e condições de saúde obtidas do cadastro do animal.
- Permitir o cadastro de novos agendamentos (`POST`) e a conclusão/registro clínico detalhado (`PATCH` / `POST`) integrados ao Xano com feedback via `rx.toast`.
- Acompanhar a evolução de peso e os custos veterinários registrados nos atendimentos concluídos.

**Non-Goals:**
- Criar novas colunas ou tabelas no banco de dados do Xano além da modelagem existente de `ATENDIMENTO_VETERINARIO` e `ANIMAL`.
- Excluir registros históricos de atendimentos já realizados (preservação clínica).
- Duplicar o componente de menu lateral fora de `sidebar_administracao()`.

## Decisions

### 1. Arquitetura Modular (`atendimento_vet_state.py` e `atendimento_vet.py`)

A implementação separa o gerenciamento de estado da camada de apresentação:
- **`ProjetoONG/atendimento_vet_state.py` (`AtendimentoVetState`):** gerencia a listagem de atendimentos e animais carregados do Xano, a data/período selecionado na agenda, os filtros de status/busca, o animal ativo no painel clínico e os campos dos modais de agendamento e conclusão clínica.
- **`ProjetoONG/atendimento_vet.py` (`pagina_atendimento_vet`):** renderiza o layout dividido junto ao `sidebar_administracao()`, contendo a Agenda Clínica, o Painel Clínico do Animal Selecionado e os modais de ação.
- **`ProjetoONG/ProjetoONG.py`:** registra a rota `/atendimento-vet` vinculada ao `on_load` para carregamento automático dos dados.

### 2. Organização da Interface em Duas Áreas

- **Área Esquerda — Agenda Clínica:**
  - Controles de navegação por data/semana, filtro por status (`Agendado`, `Realizado`, `Cancelado`) e botão de ação rápida **"Novo Agendamento"**.
  - Grade de horários/turnos apresentando os agendamentos com badges de status separados da identificação visual por tipo de procedimento:
    - **Verde:** vacinação.
    - **Vermelho:** cirurgia.
    - **Amarelo/Âmbar:** consulta.
- **Área Direita — Ficha Clínica Resumida e Histórico:**
  - Cabeçalho do animal selecionado com fotografia (`foto_url` com fallback seguro), nome, espécie, raça, idade estimada e sexo.
  - Faixa de **Alertas Clínicos** destacando `condicao_saude`, `alergias` e `restricoes_clinicas` vindos da entidade `ANIMAL`.
  - Lista dos **3 atendimentos realizados mais recentes** (data, procedimento, diagnóstico, peso e veterinário responsável) e botão/modal para consultar o **histórico veterinário completo** do pet.

### 3. Persistência e Ciclo de Vida do Atendimento (`Xano`)

- Os registros utilizam os campos da entidade `ATENDIMENTO_VETERINARIO`: `id`, `animal_id`, `data_atendimento`, `horario_atendimento`, `diagnostico`, `procedimentos`, `tratamento`, `custo`, `veterinario_responsavel`, `peso` e `status_atendimento`.
- Enquanto `status_atendimento` estiver como `Agendado`, campos clínicos como `diagnostico`, `tratamento`, `custo` e `peso` podem permanecer vazios, sendo preenchidos no momento da conclusão do atendimento (`Realizado`) via `PATCH`.
- Todas as chamadas HTTP utilizam `httpx.AsyncClient` com token JWT (`Authorization: Bearer <token>`) e URLs configuradas no `.env`.

### 4. Identidade Visual Institucional

A interface segue a paleta unificada da Área Administrativa (Areia `#EFE6DA`, Bege Claro `#F8F3EC`, Terracota `#A96348` / `#A65F43`, Verde Oliva `#737747` e Café Escuro `#2D1F18`), reservando os acentos verde, vermelho e amarelo exclusivamente para a codificação clínica dos procedimentos e alertas médicos.

## Risks / Trade-offs

- **Animal sem foto ou sem alertas cadastrados** → aplicados fallbacks visuais seguros (ícone/avatar padrão e indicador "Sem restrições conhecidas") para manter a consistência do prontuário.
- **Campos clínicos vazios em agendamentos futuros** → tratados na renderização da agenda e do histórico para exibir apenas registros concluídos na lista de "3 atendimentos mais recentes".
- **Falha de comunicação ou token expirado** → tratados com `try/except` e notificações orientativas via `rx.toast`.

## Migration Plan

1. Configurar as URLs dos endpoints de `ATENDIMENTO_VETERINARIO` e `ANIMAL` no `.env`.
2. Implementar `AtendimentoVetState` em `ProjetoONG/atendimento_vet_state.py` e `pagina_atendimento_vet` em `ProjetoONG/atendimento_vet.py`.
3. Registrar a rota `/atendimento-vet` em `ProjetoONG/ProjetoONG.py` conectada ao `sidebar_administracao()` e ao evento `on_load`.
4. Validar o fluxo completo de agendamento, navegação na agenda, seleção do pet, exibição de alertas clínicos e registro/conclusão de atendimento no Xano.