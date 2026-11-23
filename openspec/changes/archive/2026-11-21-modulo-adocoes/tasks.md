# Tasks: Módulo de Adoções

## 1. Implementação do Estado e Integração com Xano (`ProjetoONG/adocoes_state.py`)

- [x] 1.1 Criar a classe `AdocoesState` herdando de `rx.State` (ou estado base autenticado) para gerenciar os processos de adoção.
- [x] 1.2 Implementar o carregamento assíncrono (`httpx`) autenticado via token JWT (`LoginState.token`) consultando os processos de adoção e dados relacionados de pet e tutor no Xano.
- [x] 1.3 Implementar variáveis de filtro (`busca_termo`, `filtro_status`) e o getter reativo (`@rx.var adocoes_filtradas`) para filtragem em tempo real por solicitante, pet e status.
- [x] 1.4 Implementar a seleção de solicitação ativa (`selecionar_solicitacao`) e o preenchimento automático dos campos de detalhe.
- [x] 1.5 Implementar as ações de abertura do modal e salvamento autenticado (`PATCH` no Xano) para edição controlada de contatos do tutor (`telefone`, `email`, `endereco`) com feedback via `rx.toast`.
- [x] 1.6 Implementar a ação de atualização de status do processo de adoção (`Em análise`, `Aprovada`, `Adoção efetivada`, `Recusada`) integrada via `PATCH` ao Xano com sincronização da lista e aviso via `rx.toast`.

## 2. Implementação da Interface Master-Detail (`ProjetoONG/adocoes.py`)

- [x] 2.1 Construir a página `pagina_adocoes` integrada ao menu lateral unificado `sidebar_administracao()` e à paleta institucional da Área Administrativa.
- [x] 2.2 Montar o layout Master-Detail (~35% / ~65%) com tratamento de estados vazios e carregamento.
- [x] 2.3 Montar a Coluna Esquerda — Master (~35%): barra de busca textual, seletor de filtro por status e lista rolável de cartões interativos com destaque para o item selecionado.
- [x] 2.4 Montar a Coluna Direita — Detail (~65%): exibição detalhada do animal solicitado, dados cadastrais do tutor com CPF bloqueado (`disabled=True` / somente leitura) e questionário de triagem em modo estritamente somente leitura.
- [x] 2.5 Adicionar os controles de alteração de status do processo de adoção e o botão "Editar Contatos" no painel de detalhes.
- [x] 2.6 Criar a janela modal para edição restrita dos contatos do tutor (telefone, e-mail e endereço).

## 3. Integração, Roteamento e Validação (`ProjetoONG/ProjetoONG.py`)

- [x] 3.1 Registrar a rota `/adocoes` em `ProjetoONG/ProjetoONG.py` (`app.add_page`) com disparo automático de carregamento no ciclo `on_load`.
- [x] 3.2 Validar a filtragem em tempo real, a alternância Master-Detail e o bloqueio de edição de campos sensíveis (CPF e questionário).
- [x] 3.3 Testar a persistência das edições de contato e atualizações de status junto ao backend Xano e confirmar a ausência de erros de compilação.