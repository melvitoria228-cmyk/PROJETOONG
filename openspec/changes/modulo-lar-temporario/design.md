# Design — Gestão de Lares Temporários

## Contexto

O módulo de Lares Temporários permitirá ao administrador consultar os lares cadastrados, acompanhar sua capacidade e gerenciar a permanência dos animais acolhidos.

A implementação seguirá as entidades `LAR_TEMPORARIO`, `ANIMAL` e `ANIMAL_LAR_TEMPORARIO`, respeitando os relacionamentos e as regras definidos na documentação do sistema.

## Decisões de Design

### 1. Organização da tela

A tela será organizada em:

- Indicadores de ocupação dos lares.
- Cards com as informações dos lares temporários.
- Filtros para consulta dos lares.
- Ações para consultar a ficha e alocar animais.

Os cards apresentarão responsável, endereço, capacidade e quantidade de animais acolhidos.

### 2. Controle de capacidade

A quantidade de animais acolhidos será calculada com base nos registros de `ANIMAL_LAR_TEMPORARIO` que ainda não possuem data de encerramento (`data_fim`).

A disponibilidade de vagas será calculada pela diferença entre a capacidade cadastrada do lar e a quantidade de animais atualmente acolhidos.

O sistema deverá impedir novas alocações quando a capacidade máxima for atingida.

### 3. Alocação e saída de animais

A alocação será registrada em `ANIMAL_LAR_TEMPORARIO`, vinculando o animal ao lar temporário e registrando a data de início da permanência.

Na saída, será registrada a data de encerramento (`data_fim`), preservando o histórico.

Em caso de transferência, a permanência anterior será encerrada e um novo registro será criado para o lar de destino.

### 4. Consulta do histórico

O histórico será obtido pelos registros de `ANIMAL_LAR_TEMPORARIO`, apresentando as datas de início, encerramento e observações de cada permanência.

### 5. Integração com o backend

A aplicação utilizará os dados disponibilizados pelo Xano para consultar os lares, os animais e os registros de permanência.

As operações de consulta, alocação, saída e transferência deverão respeitar as regras de capacidade e preservação do histórico.

## Considerações

- O endereço cadastrado em `LAR_TEMPORARIO` será utilizado para apresentar a localização do lar e apoiar os filtros.
- A documentação não define um campo específico de bairro ou região.
- A entidade `LAR_TEMPORARIO` não possui um campo de status ativo. Portanto, o indicador de lares ativos deverá ser definido conforme os dados efetivamente disponíveis, sem criar um novo campo nesta etapa.
