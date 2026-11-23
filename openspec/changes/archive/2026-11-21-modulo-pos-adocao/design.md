# Design: Módulo de Pós-Adoção

## Context

O módulo de **Pós-Adoção** integra a Área Administrativa do **Porto Seguro Pet** (rota `/pos-adocao`) e permite que a equipe da ONG acompanhe a adaptação dos animais após a conclusão do processo de adoção, centralizando visitas, contatos e orientações repassadas aos tutores.

Para evitar redundância visual com o padrão Master-Detail do módulo de Adoções, a interface adota um layout de duas colunas (~30% / ~70%) focado em uma **Linha do Tempo (Timeline)** cronológica decrescente, conectando-se de forma autenticada via JWT às entidades `PROCESSO_ADOCAO`, `ANIMAL`, `TUTOR_ADOTANTE` e `ACOMPANHAMENTO_POS_ADOCAO` no backend **Xano** e compartilhando o menu lateral fixo `sidebar_administracao()` em `ProjetoONG.py`.

## Goals / Non-Goals

### Goals

- Disponibilizar a interface administrativa de Pós-Adoção na rota `/pos-adocao` com carregamento automático (`on_load`) e layout dividido (~30% / ~70%).
- Filtrar e exibir na coluna esquerda (~30%) exclusivamente os processos de adoção cujo `status_processo` seja `Adoção efetivada`, permitindo busca por nome do animal ou do tutor.
- Exibir na coluna direita (~70%) o cabeçalho resumido do animal e do tutor selecionados (nome, contato e endereço, quando disponível) e a **Linha do Tempo (Timeline)** de acompanhamentos em ordem cronológica decrescente (do mais recente para o mais antigo).
- Permitir incluir novos registros de acompanhamento (`POST` em `ACOMPANHAMENTO_POS_ADOCAO`) vinculados ao `processo_adocao_id` selecionado, com atualização imediata da timeline e feedback via `rx.toast`.
- Isolar a rolagem vertical individualmente na lista de cards e no feed da timeline, evitando barras de rolagem desnecessárias no viewport principal (`height="100vh"`, `overflow="hidden"`).

### Non-Goals

- Exibir processos de adoção que ainda estejam `Em análise`, `Aprovada` ou `Recusada` (escopo exclusivo do módulo de Adoções).
- Criar novas colunas ou alterar a estrutura das tabelas existentes no banco de dados do Xano.
- Duplicar o componente de menu lateral fora de `sidebar_administracao()`.

## Decisions

### 1. Arquitetura Modular (`pos_adocao_state.py` e `pos_adocao.py`)

A implementação separa o gerenciamento de estado da camada visual:
- **`ProjetoONG/pos_adocao_state.py` (`PosAdocaoState`):** carrega do Xano os processos com `status_processo == "Adoção efetivada"`, resolve os dados relacionados de animal e tutor, gerencia o filtro textual da lista, controla o processo ativo selecionado e executa o envio (`POST`) de novos registros em `ACOMPANHAMENTO_POS_ADOCAO`.
- **`ProjetoONG/pos_adocao.py` (`pagina_pos_adocao`):** renderiza o layout integrado ao `sidebar_administracao()` (`grid_template_columns="230px 1fr"`, `height="100vh"`, `overflow="hidden"`), contendo a coluna de animais adotados (~30%), a coluna da Timeline (~70%) e o formulário/modal de novo registro.
- **`ProjetoONG/ProjetoONG.py`:** registra a rota `/pos-adocao` disparando o carregamento inicial no ciclo `on_load`.

### 2. Estrutura Visual em Duas Colunas e Timeline

- **Coluna Esquerda (~30% — Lista de Animais Adotados):**
  - Campo de pesquisa em tempo real por nome do animal ou do tutor.
  - Cards selecionáveis apresentando foto em miniatura (com fallback seguro), nome do animal, nome e telefone do tutor e badge de status `Adoção efetivada`.
- **Coluna Direita (~70% — Timeline de Acompanhamento):**
  - Cabeçalho destacando o animal selecionado, dados de contato e endereço do tutor (quando disponível) e botão de ação primária **`+ Adicionar Novo Registro`**.
  - Feed cronológico vertical exibindo os registros de `ACOMPANHAMENTO_POS_ADOCAO` ordenados do mais recente para o mais antigo, com `data_acompanhamento` e `relatorio_observacao`.
  - Formulário/modal para registrar novo acompanhamento informando data e relatório de observação vinculados ao `processo_adocao_id` ativo.

### 3. Modelo de Dados e Integração Autenticada com o Xano

- **Entidades utilizadas:** `ACOMPANHAMENTO_POS_ADOCAO` (`id`, `data_acompanhamento`, `relatorio_observacao`, `processo_adocao_id`), `PROCESSO_ADOCAO` (`status_processo == "Adoção efetivada"`, `animal_id`, `tutor_adotante_id`), `ANIMAL` e `TUTOR_ADOTANTE`.
- **Comunicação HTTP:** requisições assíncronas (`httpx.AsyncClient`) autenticadas com cabeçalho `Authorization: Bearer <token>` obtido de `LoginState.token` e URLs configuradas no `.env`, com notificações via `rx.toast`.

### 4. Identidade Visual Institucional

A interface segue a paleta unificada da Área Administrativa:
- Fundo global Bege Claro (`#F8F3EC`) e menu lateral Areia (`#EFE6DA`).
- Ações e botões principais em Café Escuro (`#58392B`, hover `#422A1F`) harmonizados com os tons institucionais Terracota (`#A96348`) e Verde Oliva (`#737747`).

## Risks / Trade-offs

- **Animal sem foto ou tutor sem endereço cadastrado** → Tratados com fallbacks visuais seguros no `PosAdocaoState` para manter a integridade do layout dos cards e do cabeçalho.
- **Falha de comunicação ou token expirado durante gravação (`POST`)** → Interceptados com blocos `try/except`, mantendo o estado anterior íntegro e exibindo aviso via `rx.toast`.

## Migration Plan

1. Configurar as URLs dos endpoints de `PROCESSO_ADOCAO`, `ANIMAL`, `TUTOR_ADOTANTE` e `ACOMPANHAMENTO_POS_ADOCAO` no `.env`.
2. Implementar `PosAdocaoState` em `ProjetoONG/pos_adocao_state.py` e `pagina_pos_adocao` em `ProjetoONG/pos_adocao.py`.
3. Registrar a rota `/pos-adocao` em `ProjetoONG/ProjetoONG.py` conectada ao `sidebar_administracao()` e ao evento `on_load`.
4. Validar o filtro exclusivo de adoções efetivadas, a busca por animal/tutor, a ordenação decrescente da timeline e a persistência de novos registros no Xano.