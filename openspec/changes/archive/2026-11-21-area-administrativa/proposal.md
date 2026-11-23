# Proposal: Área Administrativa

## Problema

O sistema Porto Seguro Pet precisa de uma área administrativa centralizada, organizada e responsiva que permita à equipe da ONG gerenciar todo o ciclo operacional da instituição — desde o resgate e acolhimento dos animais até a efetivação da adoção, acompanhamento pós-adoção, gestão de voluntários e controle de doações.

Inicialmente, o sistema contava apenas com telas estáticas e dependia de navegação interna em uma única rota. Era necessário estruturar rotas dedicadas por módulo, unificar o menu lateral de navegação (`sidebar_administracao`) e integrar os fluxos operacionais diretamente com a API do Xano.

## Objetivo

Consolidar a arquitetura da Área Administrativa do Porto Seguro Pet, tendo a rota `/administrativo` como painel de boas-vindas institucional e oferecendo navegação fluida para todas as rotas operacionais (`/animais`, `/lares-temporarios`, `/atendimento-vet`, `/adocoes`, `/pos-adocao`, `/voluntarios` e `/doacoes`).

Todos os módulos principais operam com gerenciamento de estado dedicado em Reflex e integração ativa com os endpoints do Xano, garantindo consistência de dados, feedback visual ao usuário e identidade visual padronizada.

## Escopo

A Área Administrativa apresenta navegação lateral fixa (`sidebar_administracao`) organizada por categorias funcionais:

- **PRINCIPAL:**
  - **Início (`/administrativo`)** — painel de boas-vindas institucional com visão geral da ONG, missão, funcionalidades do sistema, público-alvo e apresentação da Área do Tutor.
  - **Gestão de Animais (`/animais`)** — gerenciamento completo (CRUD) dos animais resgatados, com suporte a filtros, paginação, imagem via URL (`foto_url`) e modal de ampliação da foto.
  - **Lares Temporários (`/lares-temporarios`)** — gerenciamento dos cuidadores, vagas e histórico de acolhimento temporário integrado ao `LaresTemporariosState`.
- **ATENDIMENTO:**
  - **Atendimento Veterinário (`/atendimento-vet`)** — consulta, registro e acompanhamento de prontuários, vacinas e procedimentos veterinários.
  - **Adoções (`/adocoes`)** — gerenciamento das solicitações de adoção, análise de compatibilidade, atualização de etapas do processo e listagem de interessados (`AdocoesState`).
  - **Pós-Adoção (`/pos-adocao`)** — registro e acompanhamento das visitas e relatórios de adaptação dos animais após a adoção.
- **ADMINISTRAÇÃO:**
  - **Voluntários (`/voluntarios`)** — cadastro, consulta e gerenciamento da equipe de voluntários (`VoluntariosState`).
  - **Doações (`/doacoes`)** — controle de doadores e registro de contribuições financeiras ou materiais recebidas pela ONG (`DoacoesState`).

## Fora do escopo

Nesta entrega acadêmica não estão contemplados:

- upload direto de arquivos binários de imagem para o servidor (utilizando o link de imagem via URL em texto no campo `foto_url`);
- controle granular de permissões administrativas por subperfis (ex.: diferenciar acesso de veterinário e recepcionista dentro da área administrativa);
- relatórios analíticos exportáveis em PDF/Excel diretamente pelo painel.

## Resultado esperado

Ao final desta implementação, o Porto Seguro Pet dispõe de uma Área Administrativa completa, modular e visualmente padronizada (paleta Terracota, Verde Oliva e Areia), com menu lateral unificado, rotas dedicadas para cada operação da ONG e integração funcional com a API do Xano.