# Tasks: Módulo de Pós-Adoção (Timeline de Acompanhamento)

## Phase 1: OpenSpec & Compliance

- [ ] 1.1. Revisar `proposal.md`, `design.md` e `specs/pos-adocao/spec.md`, garantindo que estejam alinhados à estrutura atual do banco de dados.
- [ ] 1.2. Executar `openspec validate modulo-pos-adocao` e corrigir eventuais problemas de validação.

## Phase 2: Backend State (`state/pos_adocao_state.py`)

- [ ] 2.1. Criar a classe `PosAdocaoState` herdando de `rx.State`.
- [ ] 2.2. Definir os estados necessários para armazenar:
  - Lista de processos de adoção efetivados.
  - Informações dos animais relacionados aos processos.
  - Informações dos respectivos tutores.
  - Registros de acompanhamento do processo selecionado.
  - Identificador do processo de adoção selecionado.
  - Dados do formulário de novo acompanhamento.
  - Estados de carregamento, mensagens e erros.
- [ ] 2.3. Criar os handlers para carregar os processos de adoção efetivados, selecionar um animal e consultar seus registros de acompanhamento.
- [ ] 2.4. Implementar a abertura e o fechamento do formulário de novo registro.
- [ ] 2.5. Implementar o método `adicionar_registro()` para incluir um acompanhamento vinculado ao processo de adoção selecionado.

## Phase 3: Integration with Xano (API / Database)

- [ ] 3.1. Utilizar a estrutura existente da tabela `ACOMPANHAMENTO_POS_ADOCAO`, considerando os campos `id`, `data_acompanhamento`, `relatorio_observacao` e `processo_adocao_id`.
- [ ] 3.2. Integrar a consulta dos processos de adoção com status `Adoção efetivada`.
- [ ] 3.3. Obter as informações dos animais e tutores por meio dos relacionamentos existentes em `PROCESSO_ADOCAO`.
- [ ] 3.4. Integrar a consulta dos registros de acompanhamento vinculados ao processo de adoção selecionado.
- [ ] 3.5. Integrar a gravação de novos acompanhamentos, vinculando cada registro ao respectivo processo de adoção.
- [ ] 3.6. Ordenar os registros de acompanhamento por `data_acompanhamento`, do mais recente para o mais antigo.

## Phase 4: Frontend UI (`modulos_administracao/pos_adocao.py`)

- [ ] 4.1. Configurar o layout principal com duas colunas, preservando as cores Porto Seguro Pet V5 (`#F8F3EC` no fundo e `#EFE6DA` na sidebar).
- [ ] 4.2. Integrar a sidebar e o menu lateral da área administrativa.
- [ ] 4.3. Construir a Coluna Esquerda (~30%):
  - Campo de pesquisa por nome do animal ou tutor.
  - Lista de processos de adoção efetivados.
  - Cards com foto e nome do animal, nome do tutor e telefone de contato.
- [ ] 4.4. Construir a Coluna Direita (~70%):
  - Cabeçalho com as informações do animal selecionado e os dados de contato do tutor.
  - Botão `[ + Adicionar Novo Registro ]`.
  - Timeline com data e relatório de observação dos acompanhamentos, em ordem cronológica decrescente.
  - Mensagem informativa quando não houver registros de acompanhamento.
- [ ] 4.5. Construir o formulário para inclusão de novo acompanhamento, contendo data e relatório de observação.

## Phase 5: Routing & Validation

- [ ] 5.1. Registrar a rota `/pos-adocao` em `ProjetoONG.py`, com opção de retorno à rota `/administrativo`.
- [ ] 5.2. Testar a seleção de animais, a consulta do histórico e a inclusão de novos acompanhamentos.
- [ ] 5.3. Verificar a organização da rolagem na lista de animais e na timeline.
- [ ] 5.4. Executar `openspec validate modulo-pos-adocao` e corrigir eventuais problemas encontrados.
