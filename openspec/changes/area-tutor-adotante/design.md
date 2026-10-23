# Design: Área do Tutor/Adotante

## Context

A Área do Tutor/Adotante no sistema Porto Seguro Pet (rota `/tutor`) foi desenhada para oferecer um painel centralizado, claro e acolhedor ao usuário autenticado. 

A interface busca resolver o problema da falta de clareza no status da adoção e no gerenciamento das informações pessoais, integrando o frontend em Reflex diretamente aos endpoints do Xano.

A tela principal do tutor organiza-se em duas colunas centrais: a coluna esquerda com o bloco cadastral e atalhos de serviços, e a coluna direita com o feed visual das solicitações de adoção.

## Goals / Non-Goals

### Goals
- Centralizar o acesso do tutor na rota `/tutor` com navegação dedicada e botão de logout.
- Apresentar 3 cartões/blocos de serviços e gerenciamento: "Meus Dados", "Acompanhamento" e "Orientações".
- Exibir os processos de adoção reais com identificação visual do animal (nome do pet via Add-on do Xano) em vez de apenas o código numérico.
- Apresentar a evolução da solicitação por meio de um indicador visual de progresso por etapas (1. Análise, 2. Aprovação, 3. Conclusão) com mensagens explicativas.
- Permitir a visualização e edição completa do perfil do tutor na subpágina `/meus-dados` integrada ao Xano.
- Manter a identidade visual da ONG utilizando a paleta grafite (`#2D3142`), creme (`#FFF7ED` / `#F4E7D5`) e terracota (`#D78A45`).

### Non-Goals
- Criar rotas ou telas para funcionalidades administrativas dentro do ambiente do tutor.
- Criar tabelas desnecessárias no banco para representar elementos exclusivamente visuais.
- Exibir fotos ou informações de animais que não estejam vinculados no backend.

## Decisions

- **Divisão Visual em 2 Colunas (`ProjetoONG.py`):**
  - **Coluna Esquerda:** Bloco de resumo de perfil com atalho para edição, seguido pelos cartões de navegação "Acompanhamento" (`/acompanhamento`) e "Orientações" (`/orientacoes`).
  - **Coluna Direita:** Feed de "Minhas Adoções" com cards detalhados por solicitação.
- **Relacionamento via Add-on no Xano:** Utilizar o Add-on no endpoint GET de processos de adoção para injetar o objeto do animal (`_animal`) e exibir seu nome no cabeçalho do card de adoção.
- **Indicador Visual por Etapas (Stepper 1-2-3):** Mapear o campo `status_processo` em 3 passos gráficos e caixas de texto informativas para orientar o tutor sobre o que esperar de cada fase.
- **Integração de Perfil no `/meus-dados`:** Formulário de edição dos dados pessoais (`nome`, `cpf`, `telefone`, `tipo_residencia`, `endereco`) integrado ao endpoint PATCH do Xano.
- **Padrão de Navegação com Botão Voltar:** Incluir links de retorno interativos em todas as subpáginas para garantir retorno simples ao painel `/tutor`.

## Risks / Trade-offs

- **Dados de Animal Ausentes:** Caso o retorno do Add-on do Xano venha vazio, a interface aplica fallbacks seguros (`Animal #ID` ou `Pet em Processo`).
- **Sessão Expirada:** Tratar erros de autenticação na consulta e edição com redirecionamento/avisos via `rx.toast`.

## Migration Plan

1. Manter a rota principal do tutor em `/tutor`.
2. Validar a renderização do feed de adoções com o nome do pet vindo do Add-on.
3. Garantir o funcionamento das rotas dos 3 cartões/blocos (`/meus-dados`, `/acompanhamento`, `/orientacoes`).
4. Testar a atualização dos dados do tutor com o backend Xano.