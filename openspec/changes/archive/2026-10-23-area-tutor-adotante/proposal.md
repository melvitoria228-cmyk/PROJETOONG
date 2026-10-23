# Proposal: Área do Tutor/Adotante


## Why

O sistema Porto Seguro Pet precisa oferecer um painel inicial centralizado, enxuto e objetivo para os tutores e adotantes na rota `/tutor`. 

A experiência foi desenhada para priorizar o que é mais crítico para o tutor: acompanhar com transparência a evolução das suas solicitações de adoção e manter seus dados de contato e residência sempre atualizados para a equipe da ONG.

Anteriormente, o tutor via apenas códigos numéricos e informações isoladas sobre suas solicitações. Era necessário tornar a consulta de adoções visualmente clara e explicativa, destacar a identificação real do animal resgatado, permitir que o tutor gerencie seus próprios dados cadastrais e oferecer acesso aos serviços de acompanhamento pós-adoção e orientações.

## What Changes

- Manter o painel do Tutor/Adotante registrado e acessível na rota `/tutor` com redirecionamento automático após o login conforme o perfil.
- Organizar a interface em duas colunas: bloco de dados e cartões de serviços à esquerda, e o feed visual de solicitações de adoção à direita.
- Disponibilizar os 3 cartões/blocos de navegação para subpáginas específicas: "Meus dados" (`/meus-dados`), "Acompanhamento" (`/acompanhamento`) e "Orientações" (`/orientacoes`).
- Exibir o nome real do animal em cada processo de adoção, utilizando os dados injetados via Add-on no endpoint do Xano.
- Apresentar a evolução da solicitação de adoção através de uma barra de progresso visual em 3 passos (1. Análise, 2. Aprovação, 3. Conclusão) com explicações sobre cada etapa.
- Permitir a consulta e edição dos dados pessoais do tutor na página `/meus-dados` com salvamento direto no backend Xano via requisição `PATCH`.
- Disponibilizar a visualização dos relatórios de visitas de acompanhamento pós-adoção e o guia informativo de guarda responsável.

## Capabilities

### New Capabilities

- `area-tutor-adotante`: define a estrutura visual, os cartões de navegação e a exibição clara das solicitações de adoção e perfil na área do tutor.

### Modified Capabilities

- `processo-adocao-consulta`: atualizada para incluir a identificação visual do animal e o indicador de progresso por etapas.
- `tutor-perfil-atualizacao`: permite ao tutor atualizar suas informações de contato e endereço no sistema.

## Impact

- **Frontend Reflex (`ProjetoONG.py`):** implementação da página principal `/tutor` e das subpáginas `/meus-dados`, `/acompanhamento` e `/orientacoes`, incluindo componentes de stepper e formulário com feedback via toast.
- **Backend Xano:** uso do Add-on no endpoint de listagem de `PROCESSO_ADOCAO` para retornar os dados do `ANIMAL` e uso do endpoint `PATCH /tutor_adotante` para atualização cadastral.
- **Autenticação:** preservação da validação do token JWT e direcionamento de rotas baseado no perfil do usuário (`TUTOR/ADOTANTE`).
- **Documentação OpenSpec:** sincronização da proposta para refletir as funcionalidades concluídas e os comportamentos reais da API.