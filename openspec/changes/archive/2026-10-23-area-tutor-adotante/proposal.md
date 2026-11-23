# Proposal: Área do Tutor/Adotante

## Why

O sistema Porto Seguro Pet precisa oferecer um painel inicial centralizado, acolhedor, legível e objetivo para os tutores e adotantes na rota `/tutor`. 

A experiência foi refatorada para eliminar a fragmentação entre várias subpáginas e priorizar o que é mais crítico para o tutor em uma única jornada fluida: acompanhar com transparência a evolução das suas solicitações de adoção, consultar relatórios de pós-adoção e orientações de guarda responsável, e manter seus dados de contato e residência sempre atualizados para a equipe da ONG.

Anteriormente, o tutor navegava entre rotas dispersas (`/tutor`, `/meus-dados`, `/acompanhamento`, `/orientacoes`) com layout em duas colunas e fontes reduzidas. Era necessário consolidar toda a experiência em uma navegação moderna por abas, garantir o carregamento automático dos dados ao entrar no painel, aplicar uma paleta visual mais suave e legível e preservar integralmente a integração com o backend Xano.

## What Changes

- Consolidar a Área do Tutor na rota `/tutor` com redirecionamento automático após o login JWT e carregamento automático dos dados via `LoginState.iniciar_painel_tutor` no evento `on_load`.
- Substituir o antigo layout fragmentado por uma interface centralizada baseada em **3 abas limpas** (*Minhas Adoções*, *Pós-Adoção e Guias*, e *Meu Perfil*), mantendo as rotas anteriores (`/acompanhamento`, `/meus-dados`, `/orientacoes`) como atalhos compatíveis que abrem diretamente a aba correspondente.
- Aplicar a nova identidade visual acolhedora da Área do Tutor baseada em **Terracota aberto (`#D9967B`)**, **Sálvia (`#7B9076`)** e **Soft White (`#FAF8F5`)** sobre o fundo temático de patinhas (`#FFF7ED`), com escala tipográfica ampliada para maior conforto de leitura.
- Exibir o nome real e os detalhes do animal em cada processo de adoção (via dados injetados por Add-on no endpoint do Xano), acompanhados de uma barra de progresso visual em 3 passos (**1. Análise**, **2. Aprovação**, **3. Conclusão**) com explicação clara de cada etapa.
- Unificar na aba **Pós-Adoção e Guias** o histórico de visitas/acompanhamentos pós-adoção e os guias de guarda responsável construídos com cartões nativos do Reflex (`card_guia_tutor`), removendo dependências de componentes externos.
- Permitir a consulta e edição dos dados pessoais e de endereço do tutor diretamente na aba **Meu Perfil**, com salvamento autenticado no backend Xano via requisição `PATCH` e feedback visual via *toast*.

## Capabilities

### New Capabilities

- `area-tutor-adotante`: define a estrutura unificada em 3 abas (*Minhas Adoções*, *Pós-Adoção e Guias*, *Meu Perfil*), a identidade visual Terracota aberto/Sálvia/Soft White, a tipografia ampliada e o carregamento automático inicial na rota `/tutor`.

### Modified Capabilities

- `processo-adocao-consulta`: atualizada para exibir a identificação real do animal, o indicador visual de progresso em 3 etapas e carregamento automático sem necessidade de ação manual.
- `tutor-perfil-atualizacao`: integrada diretamente na aba **Meu Perfil** do painel `/tutor` para consulta e atualização cadastral via `PATCH`.

## Impact

- **Frontend Reflex (`ProjetoONG.py`):** refatoração completa da interface do tutor (`area_tutor`, `aba_minhas_adocoes_tutor`, `aba_pos_adocao_e_guias_tutor`, `aba_meu_perfil_tutor` e `card_guia_tutor`), adição de `iniciar_painel_tutor` e redirecionamento compatível das rotas secundárias.
- **Backend Xano:** preservação integral dos endpoints existentes (`PROCESSO_ADOCAO` com Add-on de `ANIMAL`, `ACOMPANHAMENTO_POS_ADOCAO` e `PATCH /tutor_adotante`), sem exigir alterações no banco de dados.
- **Autenticação:** preservação da validação do token JWT e direcionamento de rotas baseado no perfil do usuário (`TUTOR/ADOTANTE`).
- **Evoluções Futuras Mapeadas:** agendamento de consultas veterinárias e registro de doações diretamente pelo tutor, aproveitando as tabelas já estruturadas no Xano.