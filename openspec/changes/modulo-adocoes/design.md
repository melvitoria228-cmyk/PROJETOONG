# Design: Módulo de Adoções

## Estrutura do Módulo

### 1. Estado da Aplicação (`porto_seguro_pet/state/adocoes_state.py`)
- **Dados:** Guarda a lista de adoções, o texto da pesquisa, o filtro de status selecionado e qual adoção está aberta na tela.
- **Filtro Automático:** Uma regra que filtra a lista de adoções em tempo real conforme o usuário digita ou troca o status.
- **Ações:**
  - `selecionar_solicitacao`: Troca a adoção exibida no painel direito.
  - `abrir_modal_edicao` e `salvar_contatos`: Abre a janela de edição e atualiza telefone, e-mail e endereço.

### 2. Tela e Componentes (`porto_seguro_pet/pages/adocoes.py`)
- **Coluna da Esquerda (~35%):** Campo de busca, filtro por status e a lista com os cards das solicitações.
- **Coluna da Direita (~65%):** Detalhes da solicitação selecionada:
  - Dados do Pet e do Tutor.
  - CPF e Respostas do Questionário desabilitados para edição (somente leitura).
  - Botão "Editar Contatos" para abrir a janela modal.
- **Janela Modal:** Formulário simples para alterar apenas e-mail, telefone e endereço.
