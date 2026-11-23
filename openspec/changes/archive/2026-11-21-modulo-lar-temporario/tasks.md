# Tasks: Módulo de Lares Temporários

## 1. Estrutura Modular e Interface Base (`ProjetoONG/lares_temporarios.py`)

- [x] 1.1 Criar o arquivo `ProjetoONG/lares_temporarios.py` com a página `pagina_lares_temporarios` integrada ao menu lateral fixo `sidebar_administracao()` e à paleta institucional da Área Administrativa (Areia, Bege Claro, Terracota e Verde Oliva).
- [x] 1.2 Implementar os cartões superiores de indicadores resumidos (lares ativos, vagas disponíveis e taxa de ocupação).
- [x] 1.3 Construir o Grid de Cards de Capacidade exibindo responsável, endereço, capacidade total, quantidade de animais acolhidos e identificação dos pets hospedados.
- [x] 1.4 Implementar os filtros de consulta por disponibilidade (`Todos`, `Com vagas`, `Capacidade máxima`) e busca textual por endereço/região.

## 2. Estado, Consulta de Dados e Ficha do Lar (`ProjetoONG/lares_temporarios_state.py`)

- [x] 2.1 Criar `LaresTemporariosState` em `ProjetoONG/lares_temporarios_state.py` integrado via `httpx` e token JWT (`LoginState.token`) aos endpoints de `LAR_TEMPORARIO`, `ANIMAL` e `ANIMAL_LAR_TEMPORARIO` no Xano.
- [x] 2.2 Identificar os animais atualmente acolhidos em cada lar a partir dos registros de `ANIMAL_LAR_TEMPORARIO` sem `data_fim`.
- [x] 2.3 Calcular dinamicamente a quantidade de vagas disponíveis por lar e os indicadores globais de ocupação.
- [x] 2.4 Implementar o modal/painel de consulta da ficha do lar temporário ("Ver Ficha") com os dados cadastrais, animais alojados e histórico cronológico de acolhimentos anteriores.

## 3. Alocação de Animais

- [x] 3.1 Implementar o modal e a seleção de animal elegível e lar temporário de destino no `LaresTemporariosState`.
- [x] 3.2 Validar a disponibilidade de vagas antes de confirmar a alocação, bloqueando lares com capacidade máxima atingida.
- [x] 3.3 Registrar a entrada do animal (`POST` em `ANIMAL_LAR_TEMPORARIO`) com `data_inicio`, recalculando a ocupação e exibindo feedback via `rx.toast`.

## 4. Saída e Transferência de Animais

- [x] 4.1 Implementar o registro de saída do animal (`PATCH` em `ANIMAL_LAR_TEMPORARIO`), preenchendo `data_fim` e observações sem excluir o registro histórico.
- [x] 4.2 Implementar o fluxo de transferência entre lares temporários, encerrando a permanência anterior (`data_fim`) e criando nova entrada (`POST`) no lar de destino com vaga disponível.
- [x] 4.3 Garantir a preservação integral dos registros anteriores de permanência (`data_inicio`, `data_fim` e `observacoes`).

## 5. Roteamento e Validação (`ProjetoONG/ProjetoONG.py`)

- [x] 5.1 Registrar a rota `/lares-temporarios` em `ProjetoONG/ProjetoONG.py` com carregamento automático no ciclo `on_load`.
- [x] 5.2 Testar os filtros de disponibilidade/localização, a alocação, a saída, a transferência de animais e a consulta do histórico junto ao Xano.
- [x] 5.3 Validar a conformidade da change com `openspec validate` e confirmar a ausência de erros de compilação.