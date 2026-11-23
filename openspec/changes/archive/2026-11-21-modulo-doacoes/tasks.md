# Tasks: Módulo de Doações

## 1. Estrutura Modular e Estado (`ProjetoONG/doacoes_state.py`)

- [x] 1.1 Criar o arquivo de estado `ProjetoONG/doacoes_state.py` (`DoacoesState`) para gerenciar doadores, doações, filtros e modais.
- [x] 1.2 Implementar os getters reativos para cálculo dos indicadores resumidos (total arrecadado financeiramente, quantidade de doações materiais e total de doadores) e filtragem do histórico.
- [x] 1.3 Definir o mapeamento dos campos das entidades `DOADOR` e `DOACAO` com vínculo `1:N` (`doador_id`).

## 2. Interface Administrativa (`ProjetoONG/doacoes.py` / `tela_doacoes.py`)

- [x] 2.1 Criar a página administrativa de Doações integrada ao menu lateral fixo `sidebar_administracao()` e à paleta institucional da Área Administrativa (Areia, Bege Claro, Terracota e Verde Oliva).
- [x] 2.2 Exibir os cartões de indicadores resumidos e os filtros de busca por nome do doador e tipo de contribuição (`Financeira` / `Material`).
- [x] 2.3 Implementar a área e o formulário/modal de cadastro e consulta de doadores (`DOADOR`), incluindo validação contra duplicidade de CPF.
- [x] 2.4 Implementar a área e o formulário/modal de registro de doações recebidas (`DOACAO`) com seleção entre tipo `Financeira` e `Material`.
- [x] 2.5 Exibir condicionalmente os campos específicos conforme o tipo selecionado (valor e forma de pagamento para `Financeira`; descrição do item e quantidade para `Material`, sem controle de estoque).
- [x] 2.6 Criar a tabela/listagem de consulta do histórico unificado de doações com identificação do doador, tipo, detalhes e data.

## 3. Integração com o Xano (`ProjetoONG/doacoes_state.py`)

- [x] 3.1 Configurar a leitura das URLs dos endpoints de `DOADOR` e `DOACAO` via `.env`.
- [x] 3.2 Implementar o carregamento assíncrono (`httpx` + token JWT `LoginState.token`) das listas de doadores e doações.
- [x] 3.3 Integrar o cadastro de novos doadores (`POST`) e o registro de doações financeiras e materiais (`POST`) ao Xano com atualização imediata da tela e feedback via `rx.toast`.

## 4. Navegação, Roteamento e Validação (`ProjetoONG/ProjetoONG.py`)

- [x] 4.1 Garantir a opção "Doações" no menu lateral unificado `sidebar_administracao()`.
- [x] 4.2 Registrar a rota `/doacoes` em `ProjetoONG/ProjetoONG.py` com carregamento automático no ciclo `on_load`.
- [x] 4.3 Testar o cadastro de doadores, o registro de doações financeiras e materiais, a filtragem do histórico e validar a change com `openspec validate`.