# Proposal: Área Administrativa

## Problema

O sistema Porto Seguro Pet precisa de uma área administrativa organizada que permita à equipe da ONG gerenciar centralidamente o ciclo de vida dos animais resgatados e acessar os demais módulos operacionais da instituição.

Anteriormente, a interface administrativa possuía apenas telas estáticas. Era necessário disponibilizar o módulo de Gestão de Animais com funcionalidades completas de consulta, cadastro, edição, exclusão e suporte à visualização expandida de fotos dos pets.

## Objetivo

Disponibilizar a estrutura da Área Administrativa do Porto Seguro Pet na rota `/administrativo`, oferecendo um menu lateral permanentemente aberto para navegação entre os módulos e o gerenciamento operacional completo dos animais resgatados.

O módulo de Gestão de Animais passa a ser funcional e integrado diretamente com os endpoints da API do Xano, enquanto a estrutura dos demais módulos serve como base para a implementação gradual.

## Escopo

A Área Administrativa apresenta os seguintes módulos divididos por seções no menu lateral:

- **PRINCIPAL:**
  - **Início** — visão geral com a missão e valores da ONG.
  - **Gestão de Animais** — gerenciamento completo (CRUD) dos animais resgatados, com suporte a filtros, paginação, foto em formato texto (`foto_url`) e modal de ampliação da imagem.
  - **Lares Temporários** — gerenciamento dos lares e histórico de acolhimento.
- **ATENDIMENTO:**
  - **Atendimento Veterinário** — consulta e registro de atendimentos veterinários.
  - **Adoções** — acompanhamento das solicitações e processos de adoção.
  - **Pós-Adoção** — registros de acompanhamento dos animais adotados.
- **ADMINISTRAÇÃO:**
  - **Voluntários** — gerenciamento do cadastro de voluntários e suas atividades.
  - **Estoque** — controle dos suprimentos e movimentações.
  - **Doações** — registros de doadores e doações financeiras.

## Fora do escopo

Nesta etapa não estão implementados:

- operações completas de cadastro e edição para os módulos que ainda não possuem endpoints ativos (Lares Temporários, Voluntários, Estoque, Doações, etc.);
- upload direto de arquivos pesados de imagem para o servidor (utilizando o link de imagem via URL em texto no campo `foto_url`);
- personalização de permissões administrativas por níveis de acesso.

## Resultado esperado

Ao final desta mudança, o sistema possui a Área Administrativa funcional com acesso organizado aos módulos operacionais e o gerenciamento completo do cadastro de animais no módulo **Gestão de Animais**, integrado perfeitamente à API do Xano.