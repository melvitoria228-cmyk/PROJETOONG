# Design: Área do Tutor/Adotante

## Context

A Área do Tutor/Adotante no sistema **Porto Seguro Pet** (rota `/tutor`) foi desenhada para oferecer um painel centralizado, acolhedor, legível e intuitivo ao usuário autenticado.

A interface resolve a fragmentação entre várias subpáginas e a falta de clareza sobre o andamento das solicitações de adoção, unificando toda a jornada do tutor em uma única página organizada por abas e integrada diretamente aos endpoints do **Xano** via token JWT.

## Goals / Non-Goals

### Goals
- Centralizar toda a experiência do tutor na rota `/tutor` com carregamento automático dos dados (`LoginState.iniciar_painel_tutor`) no `on_load` e botão de logout na barra superior.
- Organizar o conteúdo em **3 abas limpas e diretas**: *Minhas Adoções*, *Pós-Adoção e Guias* e *Meu Perfil*, mantendo compatibilidade com as rotas anteriores (`/acompanhamento`, `/meus-dados`, `/orientacoes`).
- Exibir os processos de adoção reais com identificação clara do animal (nome e dados do pet via Add-on `_animal` do Xano) em vez de apenas códigos numéricos.
- Apresentar a evolução de cada solicitação por meio de um indicador visual de progresso em 3 etapas (**1. Análise**, **2. Aprovação**, **3. Conclusão**) acompanhado de explicações sobre o status atual.
- Exibir relatórios de visitas de acompanhamento pós-adoção e orientações de guarda responsável usando cartões nativos do Reflex (`card_guia_tutor`), sem dependências externas.
- Permitir a visualização e edição dos dados pessoais e de residência diretamente na aba **Meu Perfil**, com salvamento via requisição `PATCH` no Xano.
- Aplicar a identidade visual acolhedora da Área do Tutor baseada em **Terracota aberto (`#D9967B`)**, **Sálvia (`#7B9076`)** e **Soft White (`#FAF8F5`)** sobre o fundo temático de patinhas (`#FFF7ED`), com tipografia ampliada.

### Non-Goals
- Expor rotas, menus ou ações administrativas dentro do ambiente do tutor.
- Criar tabelas auxiliares no banco de dados para elementos exclusivamente visuais.
- Utilizar componentes de terceiros que introduzam conflitos de compilação no Reflex (como `rx.accordion`).

## Decisions

- **Navegação Centralizada em 3 Abas (`ProjetoONG.py`):**
  - **Barra Superior Fixa:** exibe o logotipo institucional, a saudação personalizada ao tutor autenticado e o botão de encerramento de sessão (`LoginState.sair`).
  - **Aba 1 — Minhas Adoções (`aba_minhas_adocoes_tutor`):** feed de solicitações de adoção com identificação do pet, *stepper* visual de 3 etapas e orientações contextuais por status.
  - **Aba 2 — Pós-Adoção e Guias (`aba_pos_adocao_e_guias_tutor`):** lista os registros de acompanhamento pós-adoção vinculados ao tutor e apresenta os cartões informativos (`card_guia_tutor`) sobre adaptação, saúde e guarda responsável.
  - **Aba 3 — Meu Perfil (`aba_meu_perfil_tutor`):** formulário integrado para consulta e atualização de dados cadastrais (`nome`, `cpf`, `telefone`, `tipo_residencia`, `endereco`) via `PATCH /tutor_adotante`.
- **Carregamento Automático e Rotas de Compatibilidade:**
  - Ao acessar `/tutor`, o ciclo `on_load` dispara `LoginState.iniciar_painel_tutor`, carregando automaticamente as adoções e os acompanhamentos pós-adoção sem exigir clique manual de atualização.
  - As rotas legadas (`/acompanhamento`, `/meus-dados`, `/orientacoes`) permanecem registradas e redirecionam automaticamente para `/tutor` ativando a aba correspondente (`aba_tutor_ativa`).
- **Relacionamento via Add-on no Xano:** Utilizar o Add-on no endpoint `GET` de `PROCESSO_ADOCAO` para injetar os dados do animal (`_animal`) e exibir seu nome no cabeçalho de cada cartão de adoção.
- **Indicador Visual por Etapas (Stepper 1-2-3):** Mapear o campo `status_processo` em 3 etapas visuais conectadas (Analisando perfil → Aprovado → Concluído), destacando visualmente os passos concluídos e o atual.
- **Paleta Visual e Escala Tipográfica:**
  - **Terracota Aberto (`#D9967B` / hover `#C58166` / suave `#F6E9E2`):** destaque principal, abas ativas, botões de ação e etapas em andamento.
  - **Sálvia (`#7B9076` / suave `#E7EDE4`):** indicadores positivos, etapas concluídas e badges de confirmação.
  - **Soft White (`#FAF8F5`) sobre Fundo Temático (`#FFF7ED`):** cartões elevados sobre o plano de fundo suave com padrão de patinhas, garantindo contraste e conforto visual.
  - **Tipografia Ampliada:** títulos em `size="5"` a `"7"`, textos corridos em `size="3"` (`line_height="1.6"`) e controles interativos dimensionados para leitura confortável.

## Risks / Trade-offs

- **Dados de Animal Ausentes no Add-on:** Caso o retorno `_animal` do Xano venha vazio ou incompleto, a interface aplica fallbacks seguros (`Animal #ID` ou `Pet em Processo`) sem quebrar a renderização.
- **Sessão Expirada ou Falha de Rede:** Tratar erros de autenticação ou comunicação HTTP na consulta e edição com avisos claros via `rx.toast` e redirecionamento seguro quando necessário.

## Migration Plan

1. Consolidar o layout unificado em 3 abas na rota `/tutor` em `ProjetoONG.py`.
2. Vincular `LoginState.iniciar_painel_tutor` ao `on_load` de `/tutor` e configurar o redirecionamento compatível das rotas secundárias.
3. Validar a exibição do feed de adoções com o nome do pet vindo do Add-on, os cartões de pós-adoção/guias nativos e a atualização cadastral via `PATCH` no Xano.