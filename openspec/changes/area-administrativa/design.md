# Design: Área Administrativa

## Objetivo

Definir a estrutura visual e a organização da Área Administrativa do Porto Seguro Pet.

A implementação no frontend utiliza Reflex e backend em Xano, apresentando a estrutura de módulos com suporte à gestão operacional e visual de animais resgatados.

## Estrutura da tela

A Área Administrativa possui:

1. Um menu lateral permanentemente aberto, organizado por seções (Principal, Atendimento e Administração), com os nomes dos módulos sempre visíveis.
2. A identificação do sistema Porto Seguro Pet com o ícone institucional da ONG.
3. Os módulos administrativos organizados no menu, além do item Início.
4. Uma área superior com atalho para encerramento de sessão (*logout*).
5. Uma área principal de conteúdo ao lado do menu para exibição do módulo selecionado.
6. A tela de Gestão de Animais integrada para cadastro, listagem, atualização, exclusão e suporte visual a imagens dos pets.

## Módulos

O menu lateral apresenta os seguintes itens divididos por categorias:

- **PRINCIPAL:**
  - **Início**
  - **Gestão de Animais**
  - **Lares Temporários**
- **ATENDIMENTO:**
  - **Atendimento Veterinário**
  - **Adoções**
  - **Pós-Adoção**
- **ADMINISTRAÇÃO:**
  - **Voluntários**
  - **Estoque**
  - **Doações**

O item **Início** apresenta a visão geral da ONG com informações sobre missão e valores.

O módulo **Gestão de Animais** permite o gerenciamento completo dos cadastros com suporte a filtros, paginação, foto em formato de texto (`foto_url`) e modal de ampliação de imagem em tempo real.

Os demais módulos representam as áreas definidas no modelo de dados do Porto Seguro Pet.

## Organização visual

A interface utiliza duas áreas principais:

- **Menu lateral:** permanece sempre aberto, com os nomes dos módulos e ícones visíveis em fundo bege escuro (`#F4E7D5`).
- **Área de conteúdo:** fica ao lado do menu em fundo creme claro (`#FAF6F0`), utilizada para apresentar as informações do módulo ativo.

Na **Gestão de Animais**, a interface organiza-se em:
- **Cartões de Resumo:** total de cadastros, quantidade de cães, gatos e resgates nos últimos 30 dias.
- **Barra de Controle:** busca por nome/código, filtros por espécie, porte e status, botão de atualização e atalho para cadastro.
- **Tabela de Dados:** exibe avatar/foto circular do pet com suporte ao clique para ampliação, código, raça, porte, idade em meses, data de resgate, saúde, status com badge colorida e botões de ação (Visualizar, Editar, Excluir).
- **Modal de Ampliação:** tela pop-up para visualização da foto do pet em tamanho expandido.

A interface mantém a identidade visual definida para o Porto Seguro Pet, utilizando a paleta com grafite (`#342D29` / `#3E4149`), creme (`#FAF6F0` / `#F4E7D5`) e terracota (`#684638` / `#D78A45`).

## Navegação

Os itens do menu funcionam como seletores dinâmicos de tela no estado da aplicação (`LoginState.tela_atual`).

A seleção do módulo **Gestão de Animais** renderiza a interface interativa integrada à API do Xano via token de autenticação JWT, permitindo operações completas de criação, leitura, atualização e exclusão (CRUD).