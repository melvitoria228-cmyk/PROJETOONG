# Proposal: Módulo de Adoções

## Contexto e Motivação
Iniciar a implementação em Reflex do Módulo de Adoções, organizando a interface no padrão Master-Detail (~35% / ~65%) e garantindo o bloqueio de campos sensíveis para auditabilidade.

## Escopo
- Criar o estado `AdocoesState` com dados mockados, filtros de busca/status e controlo do modal.
- Implementar a página `adocoes.py` com lista master de solicitantes e painel de detalhe do pet/tutor.
- Travar CPF e respostas do questionário (somente leitura) e permitir edição de contatos via modal.

## Arquivos Afetados
- `porto_seguro_pet/state/adocoes_state.py`
- `porto_seguro_pet/pages/adocoes.py`
- `porto_seguro_pet/porto_seguro_pet.py`
