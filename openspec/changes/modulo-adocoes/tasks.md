# Tasks: Módulo de Adoções

## Implementação do Estado (`porto_seguro_pet/state/adocoes_state.py`)
- [x] Criar a classe `AdocoesState` herdando de `rx.State`.
- [x] Definir a lista inicial de solicitações de adoção mockadas com dados completos (pet, tutor, contatos, CPF e questionário).
- [x] Implementar variáveis de filtro (`busca_termo`, `filtro_status`) e o getter reativo (`@rx.var adocoes_filtradas`).
- [x] Implementar seleção de solicitação ativa e controle do modal de edição de contatos.

## Implementação da Interface UI (`porto_seguro_pet/pages/adocoes.py`)
- [x] Criar o layout Master-Detail (~35% / ~65%) em `adocoes.py`.
- [x] Montar a Coluna Esquerda (~35%): campo de busca, filtro por status e lista de cards interativos.
- [x] Montar a Coluna Direita (~65%): exibição dos detalhes da solicitação ativa com CPF e respostas do questionário bloqueados (`disabled=True`).
- [x] Criar a janela modal para edição restrita dos contatos (telefone, e-mail e endereço).

## Integração e Roteamento (`porto_seguro_pet/porto_seguro_pet.py`)
- [x] Registrar a página de Adoções nas rotas do Reflex (`app.add_page`).
