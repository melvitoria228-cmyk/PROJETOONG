## Context

O frontend utiliza Reflex e possui uma página de login e uma área administrativa registrada na rota `/administrativo`. A autenticação consulta o Xano para identificar o tipo de usuário. A página do Tutor/Adotante será criada na rota `/tutor`.

Os requisitos funcionais desta mudança estão definidos em `specs/area-tutor-adotante/spec.md`.

## Goals / Non-Goals

**Goals:**

* Criar uma página inicial visualmente organizada para o Tutor/Adotante.
* Registrar a página na rota `/tutor`.
* Utilizar um cabeçalho superior, uma área de boas-vindas e cartões de conteúdo.
* Aplicar a paleta de cores grafite, creme e terracota.
* Manter a interface acolhedora, com referências visuais à adoção responsável de cães e gatos.

**Non-Goals:**

* Implementar cadastro, edição ou consulta real de animais.
* Implementar solicitações ou acompanhamento funcional de adoções.
* Implementar edição dos dados pessoais do tutor.
* Alterar endpoints, tabelas ou autenticação no Xano.
* Criar funcionalidades para elementos que, nesta etapa, serão apenas visuais.

## Decisions

* **Usar Reflex:** manter a tecnologia já utilizada no frontend, sem introduzir novas dependências.
* **Criar uma função de página independente:** definir a página do Tutor/Adotante separadamente da página administrativa.
* **Registrar a rota `/tutor`:** utilizar `app.add_page` para disponibilizar a página.
* **Utilizar cabeçalho superior:** exibir a identificação “Área do Tutor/Adotante”, a marca Porto Seguro Pet e elementos visuais de perfil.
* **Não utilizar menu lateral:** organizar a navegação visual por meio de cartões na área principal.
* **Criar uma área de boas-vindas:** apresentar uma saudação e uma mensagem acolhedora relacionada à adoção.
* **Exibir quatro cartões:** “Minhas adoções”, “Acompanhamento”, “Meus dados” e “Orientações”. Nesta etapa, os cartões não executarão funcionalidades ainda não implementadas.
* **Aplicar a paleta visual:** utilizar grafite `#3E4149`, creme `#F4E7D5` e terracota `#D78A45`, com fundos claros, cartões com cantos arredondados e espaçamento confortável.
* **Manter o escopo inicial controlado:** implementar a apresentação visual sem simular dados reais ou ações funcionais.

## Risks / Trade-offs

* **A rota pode não estar registrada corretamente:** verificar a inicialização do Reflex e acessar `/tutor` no navegador.
* **O login pode reconhecer o tipo de usuário, mas a página não estar disponível:** testar o registro da rota e o redirecionamento após a autenticação.
* **Os cartões podem parecer funcionais sem serem:** deixar claro no desenvolvimento que são apenas elementos visuais nesta etapa.
* **O controle de acesso ainda não estará garantido por esta mudança:** tratar a proteção das páginas restritas separadamente.

## Migration Plan

1. Atualizar os requisitos e validar a documentação OpenSpec.
2. Implementar a página com cabeçalho superior, boas-vindas e quatro cartões.
3. Registrar a rota `/tutor`.
4. Executar a aplicação e verificar a aparência e a abertura da página.
5. Testar os redirecionamentos após o login.
6. Executar novamente a validação OpenSpec.
7. Em caso de falha, corrigir o problema antes de considerar a etapa concluída.
