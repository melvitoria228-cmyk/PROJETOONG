# Tasks: Módulo de Pós-Adoção

## 1. Conformidade OpenSpec

- [x] 1.1 Revisar `proposal.md`, `design.md` e `specs/pos-adocao/spec.md`, garantindo total alinhamento com a estrutura atual do banco de dados no Xano e a arquitetura Reflex.
- [x] 1.2 Executar `openspec validate modulo-pos-adocao` e validar a conformidade dos artefatos.

## 2. Estado e Regras de Negócio (`ProjetoONG/pos_adocao_state.py`)

- [x] 2.1 Criar a classe `PosAdocaoState` herdando de `rx.State`.
- [x] 2.2 Definir os estados e getters reativos para armazenar:
  - Lista de processos de adoção efetivados (`status_processo == "Adoção efetivada"`) e termo de pesquisa por animal/tutor.
  - Dados resolvidos dos animais (`ANIMAL`) e tutores (`TUTOR_ADOTANTE`) vinculados aos processos.
  - Registros de acompanhamento (`ACOMPANHAMENTO_POS_ADOCAO`) do processo selecionado ordenados de forma decrescente por `data_acompanhamento`.
  - Identificador do processo de adoção selecionado, campos do formulário de novo acompanhamento e estados de carregamento/feedback.
- [x] 2.3 Implementar os handlers assíncronos para carregar os processos efetivados, selecionar um animal/processo e filtrar os acompanhamentos vinculados.
- [x] 2.4 Implementar a abertura e o fechamento do formulário/modal de novo registro de acompanhamento.
- [x] 2.5 Implementar o método `adicionar_registro()` (`POST`) para gravar um novo acompanhamento vinculado ao `processo_adocao_id` selecionado com feedback via `rx.toast`.

## 3. Integração Autenticada com o Xano

- [x] 3.1 Configurar a leitura das URLs dos endpoints de `PROCESSO_ADOCAO`, `ANIMAL`, `TUTOR_ADOTANTE` e `ACOMPANHAMENTO_POS_ADOCAO` via `.env`.
- [x] 3.2 Integrar a consulta autenticada (`httpx` + token JWT `LoginState.token`) dos processos de adoção com status `Adoção efetivada` e resolver seus relacionamentos com animal e tutor.
- [x] 3.3 Integrar a consulta (`GET`) e a inclusão (`POST`) na tabela `ACOMPANHAMENTO_POS_ADOCAO` utilizando os campos existentes (`id`, `data_acompanhamento`, `relatorio_observacao`, `processo_adocao_id`), ordenando a exibição do mais recente para o mais antigo.

## 4. Interface Administrativa (`ProjetoONG/pos_adocao.py`)

- [x] 4.1 Configurar o layout principal de duas colunas (~30% / ~70%) integrado ao menu lateral fixo `sidebar_administracao()` e à paleta institucional da Área Administrativa (`#F8F3EC` no fundo, `#EFE6DA` na sidebar e `#58392B` nas ações principais).
- [x] 4.2 Construir a Coluna Esquerda (~30%):
  - Campo de pesquisa em tempo real por nome do animal ou do tutor.
  - Cards selecionáveis exibindo foto em miniatura (com fallback seguro), nome do animal, nome e telefone do tutor e status `Adoção efetivada`.
- [x] 4.3 Construir a Coluna Direita (~70%):
  - Cabeçalho com as informações do animal selecionado, contato e endereço do tutor (quando disponível) e botão `[ + Adicionar Novo Registro ]`.
  - Feed cronológico vertical (Timeline) apresentando `data_acompanhamento` e `relatorio_observacao` em ordem decrescente.
  - Mensagem informativa de estado vazio quando ainda não houver registros de acompanhamento vinculados ao processo.
- [x] 4.4 Construir o formulário/modal para inclusão de novo acompanhamento (`data_acompanhamento` e `relatorio_observacao`).

## 5. Roteamento e Validação (`ProjetoONG/ProjetoONG.py`)

- [x] 5.1 Registrar a rota `/pos-adocao` em `ProjetoONG/ProjetoONG.py` com carregamento automático no ciclo `on_load` e navegação integrada via `sidebar_administracao()`.
- [x] 5.2 Testar a seleção de animais adotados, a filtragem da lista, a visualização cronológica decrescente da timeline e a persistência de novos acompanhamentos no Xano.
- [x] 5.3 Verificar o isolamento da rolagem vertical na lista lateral e no feed da timeline sem barras desnecessárias no viewport principal.
- [x] 5.4 Executar `openspec validate modulo-pos-adocao` e confirmar ausência de erros.