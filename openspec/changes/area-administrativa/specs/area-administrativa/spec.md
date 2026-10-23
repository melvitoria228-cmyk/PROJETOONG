# Spec: Área Administrativa

## ADDED Requirements

### Requirement: Acesso à Área Administrativa

A Área Administrativa SHALL apresentar uma tela principal para acesso às áreas administrativas do sistema Porto Seguro Pet na rota `/administrativo`.

#### Scenario: Exibir a Área Administrativa
- **WHEN** o usuário do tipo `administrador` realiza login no sistema
- **THEN** o sistema redireciona para a rota `/administrativo` e apresenta a tela principal da área administrativa.

### Requirement: Exibição e organização dos módulos administrativos

A Área Administrativa SHALL apresentar os módulos principais organizados por categorias em um menu lateral permanentemente aberto.

#### Scenario: Exibir os módulos no menu lateral
- **WHEN** a Área Administrativa for carregada
- **THEN** o sistema apresenta o menu lateral organizado nas seções:
  - **PRINCIPAL:** Início, Gestão de Animais, Lares Temporários
  - **ATENDIMENTO:** Atendimento Veterinário, Adoções, Pós-Adoção
  - **ADMINISTRAÇÃO:** Voluntários, Estoque, Doações

### Requirement: Representação das áreas do sistema

Cada módulo apresentado SHALL representar uma área correspondente aos processos e entidades definidos no projeto.

#### Scenario: Identificar as áreas administrativas
- **WHEN** o usuário visualiza os módulos
- **THEN** cada módulo representa sua respectiva área do sistema.

As áreas são:
- **Animais:** `ANIMAL`
- **Lares Temporários:** `LAR_TEMPORARIO` e `ANIMAL_LAR_TEMPORARIO`
- **Atendimento Veterinário:** `ATENDIMENTO_VETERINARIO`
- **Adoções:** `PROCESSO_ADOCAO` e `TUTOR_ADOTANTE`
- **Pós-Adoção:** `ACOMPANHAMENTO_POS_ADOCAO`
- **Voluntários:** `VOLUNTARIO`, `ATIVIDADE` e `VOLUNTARIO_ATIVIDADE`
- **Estoque:** `ESTOQUE_SUPRIMENTOS` e `MOVIMENTACAO_ESTOQUE`
- **Doações:** `DOADOR` e `DOACAO`

### Requirement: Módulo de Gestão de Animais

O sistema SHALL disponibilizar o módulo operacional de Gestão de Animais integrado com o backend Xano para gerenciamento do cadastro de animais resgatados.

#### Scenario: Listagem e filtro de animais
- **WHEN** o administrador seleciona a opção "Gestão de Animais" no menu lateral
- **THEN** o sistema consulta o endpoint de listagem do Xano e exibe a tabela com código, foto/avatar, nome, espécie, sexo, raça, porte, idade estimada, data de resgate, condição de saúde e status
- **AND** permite a busca por nome/código e filtragem por espécie, porte e status.

#### Scenario: Cadastro e edição de animais com URL de foto
- **WHEN** o administrador cadastra ou edita um animal preenchendo os dados e o campo da URL da foto
- **THEN** o sistema envia os dados mapeados para os endpoints correspondentes no Xano (`POST` ou `PATCH`)
- **AND** atualiza a listagem exibindo a confirmação via *toast*.

#### Scenario: Ampliação de imagem do pet
- **WHEN** o administrador clica na foto em miniatura do pet na tabela de listagem ou no formulário
- **THEN** o sistema exibe o modal de foto expandida em tamanho ampliado.

#### Scenario: Exclusão de registro de animal
- **WHEN** o administrador confirma a exclusão de um animal no diálogo de confirmação
- **THEN** o sistema executa a requisição `DELETE` no Xano e remove o registro da listagem.

### Requirement: Navegação entre módulos

Os itens do menu lateral SHALL permitir a alteração dinâmica da tela exibida na área de conteúdo.

#### Scenario: Selecionar um módulo no menu
- **WHEN** o usuário clica em um item do menu lateral
- **THEN** o sistema atualiza a área de conteúdo para exibir a tela correspondente ao módulo selecionado.