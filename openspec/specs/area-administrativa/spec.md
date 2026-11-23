# area-administrativa Specification

## Purpose
TBD - created by archiving change area-administrativa. Update Purpose after archive.

## Requirements

### Requirement: Acesso à Área Administrativa

A Área Administrativa SHALL apresentar uma tela principal institucional na rota `/administrativo` e permitir o encerramento seguro da sessão.

#### Scenario: Exibir a Área Administrativa após login
- **WHEN** o usuário do tipo `administrador` realiza login com sucesso no sistema
- **THEN** o sistema armazena o token JWT na sessão e redireciona para a rota `/administrativo`
- **AND** exibe o painel de boas-vindas com a visão institucional da ONG (cartões *Quem somos*, *Nossa missão*, *Funcionalidades do sistema*, *Nosso público* e *Área do tutor*).

#### Scenario: Encerrar sessão administrativa
- **WHEN** o administrador clica no botão "Sair" no topo da Área Administrativa
- **THEN** o sistema limpa os dados de sessão local (`token`, `tipo_usuario`, credenciais) e redireciona para a tela inicial (`/`).

### Requirement: Exibição e organização dos módulos administrativos

A Área Administrativa SHALL apresentar os módulos principais organizados por categorias em um menu lateral permanentemente aberto (`sidebar_administracao`) em todas as páginas administrativas.

#### Scenario: Exibir os módulos no menu lateral
- **WHEN** qualquer página da Área Administrativa for carregada
- **THEN** o sistema apresenta o menu lateral fixo organizado nas seções:
  - **PRINCIPAL:** Início (`/administrativo`), Gestão de Animais (`/animais`), Lares Temporários (`/lares-temporarios`)
  - **ATENDIMENTO:** Atendimento Veterinário (`/atendimento-vet`), Adoções (`/adocoes`), Pós-Adoção (`/pos-adocao`)
  - **ADMINISTRAÇÃO:** Voluntários (`/voluntarios`), Doações (`/doacoes`)

### Requirement: Representação das áreas do sistema

Cada módulo apresentado SHALL representar uma área correspondente aos processos e entidades definidos no modelo de dados do projeto.

#### Scenario: Identificar as áreas administrativas e entidades vinculadas
- **WHEN** o usuário navega pelos módulos administrativos
- **THEN** cada módulo opera sobre suas respectivas entidades no backend Xano:
  - **Animais (`/animais`):** `ANIMAL`
  - **Lares Temporários (`/lares-temporarios`):** `LAR_TEMPORARIO` e `ANIMAL_LAR_TEMPORARIO`
  - **Atendimento Veterinário (`/atendimento-vet`):** `ATENDIMENTO_VETERINARIO`
  - **Adoções (`/adocoes`):** `PROCESSO_ADOCAO` e `TUTOR_ADOTANTE`
  - **Pós-Adoção (`/pos-adocao`):** `ACOMPANHAMENTO_POS_ADOCAO`
  - **Voluntários (`/voluntarios`):** `VOLUNTARIO`, `ATIVIDADE` e `VOLUNTARIO_ATIVIDADE`
  - **Doações (`/doacoes`):** `DOADOR` e `DOACAO`

### Requirement: Módulo de Gestão de Animais

O sistema SHALL disponibilizar o módulo operacional de Gestão de Animais na rota `/animais` integrado com o backend Xano para gerenciamento completo dos animais resgatados.

#### Scenario: Listagem e filtro de animais
- **WHEN** o administrador acessa a rota `/animais`
- **THEN** o sistema consulta o endpoint de listagem do Xano e exibe os cartões de resumo e a tabela com código, foto/avatar, nome, espécie, sexo, raça, porte, idade estimada, data de resgate, condição de saúde e status
- **AND** permite a busca por nome/código e filtragem por espécie, porte e status.

#### Scenario: Cadastro e edição de animais com URL de foto
- **WHEN** o administrador cadastra ou edita um animal preenchendo os dados e o campo da URL da foto (`foto_url`)
- **THEN** o sistema envia os dados mapeados para os endpoints correspondentes no Xano (`POST` ou `PATCH`)
- **AND** atualiza a listagem exibindo a confirmação via *toast*.

#### Scenario: Ampliação de imagem do pet
- **WHEN** o administrador clica na foto em miniatura do pet na tabela de listagem ou no formulário
- **THEN** o sistema exibe o modal de foto expandida em tamanho ampliado.

#### Scenario: Exclusão de registro de animal
- **WHEN** o administrador confirma a exclusão de um animal no diálogo de confirmação
- **THEN** o sistema executa a requisição `DELETE` no Xano e remove o registro da listagem.

### Requirement: Operação dos demais módulos administrativos integrados

Os demais módulos operacionais do menu lateral SHALL carregar e gerenciar seus dados no backend Xano por meio de seus respectivos estados (`LaresTemporariosState`, `AdocoesState`, `VoluntariosState`, `DoacoesState` e estados de atendimento/pós-adoção).

#### Scenario: Carregamento automático ao acessar módulo operacional
- **WHEN** o administrador navega para uma rota operacional (`/lares-temporarios`, `/atendimento-vet`, `/adocoes`, `/pos-adocao`, `/voluntarios` ou `/doacoes`)
- **THEN** o evento `on_load` da página dispara a consulta inicial na API do Xano utilizando o token JWT autenticado
- **AND** exibe os registros, filtros e ações operacionais correspondentes ao módulo.

### Requirement: Navegação entre módulos por rotas dedicadas

Os itens do menu lateral SHALL permitir a navegação direta entre as rotas dedicadas de cada módulo administrativo.

#### Scenario: Selecionar um módulo no menu lateral
- **WHEN** o usuário clica em um item do menu lateral (`sidebar_administracao`)
- **THEN** o sistema navega para a rota correspondente ao módulo selecionado, preservando o menu lateral visível e o estado de autenticação do administrador.
