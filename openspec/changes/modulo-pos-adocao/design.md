# Design: Módulo de Pós-Adoção (Timeline de Acompanhamento)

## 1. Visão Geral da Arquitetura Visual e UI/UX

O Módulo de Pós-Adoção adota um layout responsivo de duas colunas em formato de **Linha do Tempo (Timeline)**, evitando redundância com o padrão Master-Detail do módulo de Adoções.

### Layout Global e Cores (Paleta Porto Seguro Pet V5)

- **Fundo Global**: `#F8F3EC` (bege neutro claro e quente).
- **Sidebar Lateral**: `#EFE6DA` (tom terroso claro, sem barras de rolagem desnecessárias).
- **Container Principal**: Grid CSS (`grid_template_columns="230px 1fr"`, `height="100vh"`, `overflow="hidden"`).
- **Ações e Botões Principais**: `#58392B` (marrom escuro/café), com hover `#422A1F`.

## 2. Estrutura de Componentes

### Coluna Esquerda (~30% - Lista de Animais Adotados)

- **Filtro / Busca**: Campo de pesquisa por nome do animal ou tutor.
- **Cards Selecionáveis**:
  - Foto em miniatura e nome do animal.
  - Nome do tutor e telefone de contato.
  - Identificação dos animais vinculados a processos de adoção efetivados.
  - Indicação do status do processo: `Adoção efetivada`.

As informações do animal e do tutor serão obtidas por meio dos relacionamentos existentes entre `PROCESSO_ADOCAO`, `ANIMAL` e `TUTOR_ADOTANTE`.

### Coluna Direita (~70% - Timeline de Acompanhamento)

- **Cabeçalho do Animal Selecionado**:
  - Nome e identificação do animal.
  - Informações de contato do tutor.
  - Endereço do tutor, quando disponível.
  - Botão de ação primária: `[ + Adicionar Novo Registro ]`.

- **Feed Cronológico (Timeline Decrescente)**:
  - Data do acompanhamento.
  - Relato de observação sobre a adaptação, as condições do animal e as orientações realizadas.
  - Registros apresentados do mais recente para o mais antigo.

- **Formulário de Novo Registro**:
  - Data do acompanhamento.
  - Relatório de observação.
  - Vinculação ao processo de adoção selecionado.

## 3. Modelo de Dados e Estado (`pos_adocao_state.py`)

- **Tabela Relacionada**: `ACOMPANHAMENTO_POS_ADOCAO`.
- **Campos utilizados**:
  - `id`: identificador do registro.
  - `data_acompanhamento`: data do acompanhamento.
  - `relatorio_observacao`: descrição do acompanhamento realizado.
  - `processo_adocao_id`: referência ao processo de adoção correspondente.

- **Consulta dos Processos**: serão considerados os registros de `PROCESSO_ADOCAO` cujo `status_processo` seja `Adoção efetivada`.

- **Relacionamentos**:
  - `PROCESSO_ADOCAO.animal_id` permite consultar os dados do animal em `ANIMAL`.
  - `PROCESSO_ADOCAO.tutor_adotante_id` permite consultar os dados do tutor em `TUTOR_ADOTANTE`.

- **Gestão de Rolagem**: o isolamento da rolagem ocorre individualmente no feed da timeline e na lista de cards, evitando barras de rolagem desnecessárias no viewport principal.

A implementação utilizará os campos e relacionamentos existentes, sem exigir alterações na estrutura atual do banco de dados.
