# Design: Área Administrativa

## Objetivo

Definir a arquitetura de interface, a identidade visual, os padrões de componentes e o fluxo de navegação da Área Administrativa do **Porto Seguro Pet**.

A camada de apresentação é desenvolvida em **Reflex** (Python) e integrada ao backend no **Xano** via requisições assíncronas (`httpx`) autenticadas com token JWT, garantindo gestão operacional completa de todos os fluxos da ONG.

## Estrutura da tela

Todas as páginas da Área Administrativa compartilham uma estrutura em duas colunas (`grid` / `flex` responsivo) composta por:

1. **Menu Lateral Fixo (`sidebar_administracao`):** barra lateral permanentemente visível (`width: 260px`, `position: sticky`), com logotipo institucional do Porto Seguro Pet, categorias estruturadas e estado ativo destacado.
2. **Área Principal de Conteúdo:** container fluido (`flex: 1`) com rolagem vertical independente para exibição do painel inicial ou do módulo operacional ativo.
3. **Ação de Encerramento de Sessão:** botão de *logout* (`LoginState.sair`) no canto superior direito da área administrativa, que limpa o estado local da sessão e redireciona para a tela de autenticação (`/`).

Na tela inicial (`/administrativo`), a área de conteúdo apresenta:
- **Cabeçalho de Boas-Vindas:** saudação institucional acompanhada da ilustração animada (`/animais-boas-vindas.gif`).
- **Grade Institucional (5 Cartões Interativos):**
  - *Linha 1 (2 colunas):* **Quem somos** e **Nossa missão**.
  - *Linha 2 (3 colunas):* **Funcionalidades do sistema**, **Nosso público** e **Área do tutor**.

## Módulos

O menu lateral organiza os módulos operacionais em três categorias semânticas, cada qual vinculada a uma rota dedicada:

- **PRINCIPAL:**
  - **Início (`/administrativo`)** — visão geral institucional da ONG e apresentação do ecossistema do sistema.
  - **Gestão de Animais (`/animais`)** — CRUD completo dos animais resgatados, filtros combinados, paginação, cadastro via link de imagem (`foto_url`) e modal de ampliação da foto.
  - **Lares Temporários (`/lares-temporarios`)** — gerenciamento de cuidadores, disponibilidade de vagas e histórico de acolhimento (`LaresTemporariosState`).
- **ATENDIMENTO:**
  - **Atendimento Veterinário (`/atendimento-vet`)** — registro e acompanhamento de consultas, vacinas, exames e histórico clínico.
  - **Adoções (`/adocoes`)** — gerenciamento de solicitações de adoção, listagem lateral de candidatos com avatar unissex neutro, análise de perfil e atualização de status do processo (`AdocoesState`).
  - **Pós-Adoção (`/pos-adocao`)** — acompanhamento das visitas e relatórios de adaptação dos pets após a efetivação da adoção.
- **ADMINISTRAÇÃO:**
  - **Voluntários (`/voluntarios`)** — cadastro e organização da equipe de voluntários e suas áreas de atuação (`VoluntariosState`).
  - **Doações (`/doacoes`)** — controle de doadores e registro de contribuições financeiras ou materiais (`DoacoesState`).

## Organização visual

A Área Administrativa segue uma paleta acolhedora e institucional baseada em tons terrosos e naturais:

- **Menu Lateral:** fundo Areia (`#EFE6DA`) com borda divisória em `#E2D7C7` e destaque ativo em branco (`#FFFFFF`) com sombra sutil.
- **Área de Conteúdo:** fundo Bege Claro (`#F8F3EC`) para reduzir fadiga visual e destacar os cartões e tabelas.
- **Cores de Destaque e Ação:**
  - **Terracota Institucional:** `#A96348` / `#A65F43` (hover `#8F503B` / `#C77D5B`) e fundo suave `#F5E7DF` com borda `#E3C2B2`.
  - **Verde Oliva:** `#737747` (hover `#A3A66B`) e fundo suave `#E5E6CF` com borda `#C8CA9D`, utilizado para indicadores positivos, missão e etapas concluídas.
  - **Caramelo / Areia:** `#8C6239` / `#D6B99A` para detalhes de apoio, bordas de cartões e avatares neutros.
- **Tipografia:** Café Escuro (`#2D1F18`) para títulos e cabeçalhos; Marrom Médio (`#52433D`) para textos corridos; Cinza Quente (`#78675E` / `#9E8C82`) para subtítulos e rótulos de seção.

### Padrão Interno dos Módulos Operacionais
Os módulos compartilham componentes consistentes:
- **Cartões de Resumo (KPIs):** indicadores numéricos no topo da tela (ex.: total de animais, cães, gatos, processos em análise ou doações registradas).
- **Barra de Filtros e Ações:** campos de busca textual, seletores de filtro por categoria/status, botão de atualização e botão principal de novo cadastro.
- **Listagens, Tabelas e Painéis de Detalhe:** exibição estruturada dos registros com badges de status coloridas, avatares neutros padronizados e ações rápidas de visualização, edição e exclusão.

## Navegação

A navegação entre módulos deixou de depender exclusivamente de troca condicional de tela em uma única rota e passou a operar por meio de **rotas dedicadas** no roteador do Reflex (`app.add_page`), conectadas pelo componente `sidebar_administracao()`.

Ao acessar cada rota (`/adocoes`, `/lares-temporarios`, `/doacoes`, `/voluntarios`, etc.), o ciclo de vida `on_load` dispara automaticamente o carregamento inicial dos dados no respectivo `State` junto à API do Xano, utilizando o token JWT armazenado em `LoginState.token` para autenticação das requisições.