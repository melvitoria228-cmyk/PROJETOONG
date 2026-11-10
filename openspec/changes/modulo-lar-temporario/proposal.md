# Change: Módulo de Lares Temporários

## Why

Atualmente, o gerenciamento dos lares temporários precisa permitir que a equipe administrativa da ONG consulte a capacidade de acolhimento, identifique os animais que estão em cada lar e acompanhe a disponibilidade de vagas.

A implementação deste módulo tem como objetivo centralizar essas informações em uma interface administrativa, facilitando o gerenciamento dos lares temporários e a distribuição dos animais resgatados.

## What Changes

- Criar uma tela administrativa para gerenciamento dos lares temporários, seguindo o layout Grid de Cards de Capacidade definido na especificação de Design UI/UX V5.
- Apresentar indicadores de lares ativos, vagas disponíveis e taxa de ocupação.
- Disponibilizar filtros para visualização de todos os lares, lares com vagas, lares com capacidade máxima e localização por região ou bairro.
- Apresentar os lares em cards contendo informações do responsável, localização, capacidade e quantidade de animais acolhidos.
- Identificar os animais atualmente acolhidos em cada lar.
- Disponibilizar a ação de consultar a ficha do lar temporário.
- Disponibilizar a ação de alocar um animal em um lar temporário.
- Registrar as entradas e saídas dos animais, preservando o histórico de permanência.
- Permitir a consulta dos registros anteriores de acolhimento e das respectivas observações.

## Capabilities

### New Capabilities

- `gestao-lares-temporarios`: gerenciamento dos lares temporários, visualização de capacidade e ocupação, consulta de informações e registro de acolhimento dos animais.

## Impact

- **Interface:** criação de uma nova tela na área administrativa do Porto Seguro Pet.
- **Entidades envolvidas:** `LAR_TEMPORARIO`, `ANIMAL` e `ANIMAL_LAR_TEMPORARIO`.
- **Relacionamentos:** utilização dos relacionamentos existentes entre animais, lares temporários e registros de permanência.
- **Backend:** integração com os endpoints do Xano necessários para consultar e gerenciar os lares temporários e seus registros de acolhimento.
- **Histórico:** preservação dos registros de entrada, saída e observações dos períodos de permanência.
- **Regras de negócio:** respeito à capacidade de acolhimento dos lares e à atualização da situação dos animais durante as movimentações.

