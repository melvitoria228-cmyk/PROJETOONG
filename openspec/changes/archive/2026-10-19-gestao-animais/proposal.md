## Why

A ONG precisa organizar as informações dos animais resgatados em um local centralizado, permitindo que a equipe administrativa consulte e mantenha os registros de forma organizada. Esta mudança prepara a tela de Gestão de Animais para integrar a interface Reflex aos dados armazenados no Xano.

## What Changes

* Criar a tela administrativa de Gestão de Animais, seguindo a identidade visual definida para a área administrativa.
* Permitir consultar e visualizar os registros dos animais cadastrados.
* Permitir cadastrar novos animais resgatados e editar seus dados.
* Permitir excluir registros de animais, respeitando as regras de negócio e os relacionamentos existentes.
* Integrar as operações da tela aos endpoints de animais disponibilizados pelo Xano.
* Apresentar os dados e os estados dos animais de acordo com os campos e valores definidos no projeto.

## Capabilities

### New Capabilities

* `gestao-animais`: Consulta, cadastro, visualização, edição e exclusão de registros de animais na área administrativa, com integração ao Xano.

### Modified Capabilities

Nenhuma.

## Impact

* **Frontend:** arquivo `ProjetoONG.py`, na implementação da tela administrativa de Gestão de Animais.
* **Backend:** endpoints existentes da tabela `ANIMAL` no grupo de API `PortoSeguroPet`, no Xano.
* **Dados:** campos, estados e relacionamentos da tabela `ANIMAL` e das tabelas relacionadas.
* **Dependências:** utilização da estrutura e das dependências já existentes no projeto, sem introduzir novas dependências desnecessárias.
