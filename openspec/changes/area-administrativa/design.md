# Design: Área Administrativa

## Objetivo

Definir a estrutura visual e a organização da Área Administrativa do Porto Seguro Pet.

A implementação inicial será feita no frontend utilizando Reflex e terá como objetivo apresentar os principais módulos administrativos de forma simples e organizada.

## Estrutura da tela

A Área Administrativa deverá possuir:

1. Um menu lateral permanentemente aberto, com os nomes dos módulos sempre visíveis.
2. A identificação do sistema Porto Seguro Pet.
3. Os oito módulos administrativos organizados no menu, além do item Início.
4. Uma área principal de conteúdo ao lado do menu.
5. Um título identificando a Área Administrativa na área principal.
6. Uma área de conteúdo preparada para apresentar posteriormente as informações e funcionalidades do módulo selecionado.

## Módulos

O menu lateral deverá apresentar os seguintes itens:

* **Início**
* **Animais**
* **Lares Temporários**
* **Atendimento Veterinário**
* **Adoções**
* **Pós-Adoção**
* **Voluntários**
* **Estoque**
* **Doações**

O item **Início** representa a página inicial da Área Administrativa e não corresponde a uma tabela específica do banco de dados.

Os demais módulos representam as áreas definidas no modelo de dados e nos processos de negócio do Porto Seguro Pet.

## Organização visual

A interface deverá utilizar duas áreas principais:

* **Menu lateral:** permanecerá sempre aberto, com os nomes dos módulos visíveis. Não deverá possuir botão para recolher ou expandir o menu.
* **Área de conteúdo:** ficará ao lado do menu e será utilizada para apresentar o conteúdo da página selecionada.

A interface deverá manter a identidade visual já definida para o Porto Seguro Pet, utilizando uma aparência acolhedora, simples e profissional.

Os itens do menu deverão possuir nomes claros e, quando apropriado, elementos visuais que facilitem sua identificação.

A área de conteúdo deverá possuir espaço suficiente para que as páginas dos módulos possam ser desenvolvidas posteriormente.

## Navegação

Os itens do menu serão apresentados como pontos de acesso aos respectivos módulos.

Nesta primeira implementação, será criada a estrutura visual do menu permanentemente aberto e da área de conteúdo. As funcionalidades internas dos módulos e a navegação para suas respectivas páginas serão implementadas posteriormente.

A navegação poderá ser expandida conforme cada módulo for desenvolvido.
