# Design: Módulo de Adoções

## Context

O módulo de Adoções integra a Área Administrativa do **Porto Seguro Pet** (rota `/adocoes`) e permite que a equipe da ONG gerencie a fila de solicitações de adoção, realize a triagem de candidatos e acompanhe a evolução de cada processo até sua conclusão.

A interface comunica-se de forma assíncrona e autenticada via JWT com as tabelas `PROCESSO_ADOCAO`, `TUTOR_ADOTANTE` e `ANIMAL` no backend **Xano**, compartilhando a estrutura visual unificada pelo menu lateral fixo `sidebar_administracao()` em `ProjetoONG.py`.

## Goals / Non-Goals

**Goals:**
- Implementar a interface administrativa de adoções no padrão **Master-Detail** (~35% / ~65%) na rota `/adocoes` com carregamento automático (`on_load`).
- Permitir busca textual e filtragem em tempo real por status do processo na coluna Master.
- Exibir no painel Detail o dossiê completo da solicitação selecionada: identificação do animal resgatado, dados cadastrais do tutor/adotante e respostas do questionário de triagem.
- Garantir auditabilidade mantendo campos sensíveis (CPF e respostas declaradas no questionário) bloqueados contra edição (somente leitura).
- Permitir atualização controlada dos dados de contato do tutor (`telefone`, `email`, `endereco`) por meio de modal dedicado integrado ao Xano (`PATCH`).
- Permitir atualizar o status do processo de adoção (`Em análise`, `Aprovada`, `Adoção efetivada`, `Recusada`) com persistência imediata no Xano e feedback via `rx.toast`.

**Non-Goals:**
- Permitir a alteração manual do CPF ou das respostas originais do questionário de adoção pela equipe administrativa.
- Criar novas tabelas no banco de dados do Xano para armazenar estados temporários de interface.
- Duplicar o componente de menu lateral fora de `sidebar_administracao()`.

## Decisions

### 1. Organização Modular (`adocoes_state.py` e `adocoes.py`)

A implementação é dividida entre lógica de estado e camada de apresentação:
- **`ProjetoONG/adocoes_state.py` (`AdocoesState`):** armazena a listagem de processos de adoção carregados do Xano, os critérios de busca e filtro por status, o registro atualmente selecionado no painel Detail e os campos temporários dos modais de edição de contato e atualização de status.
- **`ProjetoONG/adocoes.py` (`pagina_adocoes`):** estrutura a tela em duas colunas junto ao `sidebar_administracao()`, renderizando o painel Master (~35%), o painel Detail (~65%) e os modais de ação.
- **`ProjetoONG/ProjetoONG.py`:** registra a rota `/adocoes` disparando o carregamento inicial no ciclo `on_load`.

### 2. Padrão Visual Master-Detail (~35% / ~65%)

- **Coluna da Esquerda — Master (~35%):** contém barra de pesquisa por nome do solicitante ou pet, seletor de filtro por status e lista rolável de cartões resumidos. O cartão selecionado recebe destaque visual na paleta institucional.
- **Coluna da Direita — Detail (~65%):** exibe os detalhes completos da solicitação ativa:
  - Resumo do animal solicitado (nome, espécie, porte e status atual).
  - Dados cadastrais do tutor/adotante com **CPF bloqueado** (`disabled=True` / somente leitura) e botão **"Editar Contatos"** para abertura do modal de atualização.
  - Bloco do questionário de triagem exibido em modo **somente leitura**, preservando a integridade das respostas submetidas pelo candidato.
  - Controles de decisão administrativa para avançar ou encerrar o status do processo (`Em análise`, `Aprovada`, `Adoção efetivada`, `Recusada`).

### 3. Integração Autenticada com o Xano

- As requisições de consulta (`GET`) e atualização (`PATCH`) utilizam `httpx.AsyncClient` com o cabeçalho `Authorization: Bearer <token>` obtido de `LoginState.token` e URLs configuradas via variáveis de ambiente no `.env`.
- Os dados relacionados do animal e do tutor (injetados via Add-on do Xano ou resolvidos na carga) são normalizados no `AdocoesState` para exibição clara sem exposição de IDs crus como única identificação.
- Após qualquer alteração de status ou atualização de contatos confirmada pelo backend, o estado local é sincronizado e o usuário recebe confirmação via `rx.toast`.

### 4. Identidade Visual Unificada

A página adota a paleta institucional da Área Administrativa:
- Menu lateral Areia (`#EFE6DA`) e fundo Bege Claro (`#F8F3EC`).
- Terracota Institucional (`#A96348` / `#A65F43`) e Verde Oliva (`#737747`) para ações principais, seleção ativa e badges de status.
- Tipografia Café Escuro (`#2D1F18`) e Marrom Médio (`#52433D`).

## Risks / Trade-offs

- **Dados relacionados incompletos no retorno do Xano** → tratados com fallbacks seguros no `AdocoesState` (`Pet não identificado` / `Solicitante #ID`) para evitar falhas de renderização.
- **Falha de comunicação ou token expirado durante atualização (`PATCH`)** → interceptados com blocos `try/except`, mantendo o estado anterior íntegro e exibindo aviso via `rx.toast`.

## Migration Plan

1. Configurar as URLs de endpoints de adoção e tutor no `.env`.
2. Implementar `AdocoesState` em `ProjetoONG/adocoes_state.py` e `pagina_adocoes` em `ProjetoONG/adocoes.py`.
3. Registrar a rota `/adocoes` em `ProjetoONG/ProjetoONG.py` conectada ao `sidebar_administracao()` e ao evento `on_load`.
4. Validar os fluxos de listagem, filtragem, seleção Master-Detail, bloqueio de campos sensíveis, edição de contatos via modal e atualização de status no Xano.