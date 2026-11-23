# Spec: Área do Tutor/Adotante

## ADDED Requirements

### Requirement: Painel Unificado e Centralizado do Tutor

O sistema SHALL centralizar a experiência do Tutor/Adotante na rota `/tutor`, organizando o conteúdo em uma navegação intuitiva por 3 abas (*Minhas Adoções*, *Pós-Adoção e Guias*, e *Meu Perfil*) com carregamento automático dos dados.

#### Scenario: Acesso e carregamento automático do painel

- **WHEN** um usuário do tipo Tutor/Adotante realiza login com sucesso ou acessa a rota `/tutor`
- **THEN** o sistema o redireciona para `/tutor` e dispara automaticamente o evento `LoginState.iniciar_painel_tutor` (`on_load`)
- **AND** carrega suas solicitações de adoção e registros de acompanhamento pós-adoção autenticados junto ao Xano.

### Requirement: Cabeçalho superior e encerramento de sessão

O sistema SHALL exibir um cabeçalho superior que identifique a marca Porto Seguro Pet, apresente a saudação ao tutor autenticado e permita o encerramento seguro da sessão (*logout*).

#### Scenario: Exibição do cabeçalho e logout

- **WHEN** a página da Área do Tutor é exibida
- **THEN** o cabeçalho apresenta a identificação institucional do Porto Seguro Pet e o nome/saudação do tutor logado
- **AND** disponibiliza o botão "Sair" (`LoginState.sair`) que limpa os dados da sessão local e redireciona para a tela inicial (`/`).

### Requirement: Navegação por abas e compatibilidade de rotas

O sistema SHALL permitir alternar entre as 3 seções principais dentro de `/tutor` sem recarregamento completo da página, mantendo compatibilidade com as rotas secundárias anteriores.

#### Scenario: Alternância entre abas no painel `/tutor`

- **WHEN** o tutor seleciona uma das abas (*Minhas Adoções*, *Pós-Adoção e Guias* ou *Meu Perfil*)
- **THEN** o sistema atualiza `LoginState.aba_tutor_ativa` e exibe imediatamente o conteúdo correspondente à aba selecionada.

#### Scenario: Acesso direto às rotas de compatibilidade

- **WHEN** o usuário ou um link externo acessa `/acompanhamento`, `/meus-dados` ou `/orientacoes`
- **THEN** o sistema redireciona para `/tutor` ativando automaticamente a aba correspondente ao serviço solicitado.

### Requirement: Consulta e exibição dos processos de adoção

O sistema SHALL permitir que o Tutor/Adotante consulte seus processos de adoção na aba *Minhas Adoções* em um feed dinâmico integrado ao Xano.

#### Scenario: Exibição dos processos de adoção

- **WHEN** a aba *Minhas Adoções* é exibida e existem processos vinculados ao tutor
- **THEN** o sistema exibe os cartões detalhados de cada solicitação de adoção carregada via token JWT do Xano.

#### Scenario: Ausência de processos de adoção

- **WHEN** o backend não retorna processos de adoção para o usuário
- **THEN** o sistema apresenta um painel informativo de estado vazio indicando que não há solicitações em andamento.

#### Scenario: Falha na consulta de adoções

- **WHEN** ocorre uma falha na consulta ao backend
- **THEN** o sistema informa ao usuário via *toast* que não foi possível carregar os processos de adoção.

### Requirement: Identificação do animal relacionado à adoção

O sistema SHALL apresentar o nome real do animal relacionado a cada processo de adoção, utilizando os dados obtidos via Add-on (`_animal`) do Xano.

#### Scenario: Identificação do animal por nome

- **WHEN** os dados da solicitação de adoção são retornados pela API com o Add-on do animal
- **THEN** o sistema exibe o nome real do animal no cabeçalho do cartão da solicitação
- **AND** caso o nome não esteja disponível, exibe uma identificação fallback segura (`Animal #ID` ou `Pet em Processo`).

### Requirement: Indicador visual de progresso da adoção (Stepper)

O sistema SHALL exibir um indicador gráfico em 3 etapas (**1. Análise**, **2. Aprovação**, **3. Conclusão**) e uma explicação textual para o status do processo.

#### Scenario: Exibição do progresso por etapa

- **WHEN** um processo de adoção é exibido
- **THEN** o sistema destaca os passos do indicador visual de acordo com o `status_processo` (`Em análise`, `Aprovada`, `Adoção efetivada`, etc.)
- **AND** apresenta uma caixa de texto explicativa detalhando a fase atual para o tutor.

### Requirement: Acompanhamento pós-adoção e Guias de Guarda Responsável

O sistema SHALL disponibilizar na aba *Pós-Adoção e Guias* o histórico de relatórios de acompanhamento pós-adoção e os cartões educativos sobre guarda responsável.

#### Scenario: Consulta do acompanhamento pós-adoção

- **WHEN** o Tutor/Adotante acessa a aba *Pós-Adoção e Guias*
- **THEN** o sistema exibe o histórico de visitas, datas e observações registradas pela equipe da ONG no Xano.

#### Scenario: Exibição dos guias educativos nativos

- **WHEN** o Tutor/Adotante visualiza a seção de orientações na aba *Pós-Adoção e Guias*
- **THEN** o sistema exibe os cartões nativos (`card_guia_tutor`) com orientações práticas sobre adaptação, saúde, alimentação e segurança do pet.

### Requirement: Edição dos dados cadastrais do Tutor

O sistema SHALL permitir que o Tutor/Adotante visualize e atualize seus dados pessoais e de endereço diretamente na aba *Meu Perfil*.

#### Scenario: Atualização dos dados cadastrais

- **WHEN** o tutor altera suas informações (`nome`, `cpf`, `telefone`, `tipo_residencia`, `endereco`) na aba *Meu Perfil* e clica em "Salvar Alterações"
- **THEN** o sistema envia uma requisição autenticada `PATCH` com os novos dados ao endpoint de atualização do tutor no Xano
- **AND** exibe uma mensagem de confirmação (*toast*) indicando o sucesso da operação.

### Requirement: Identidade visual acolhedora e tipografia legível

O sistema SHALL utilizar uma identidade visual acolhedora baseada nas cores Terracota aberto, Sálvia e Soft White sobre fundo temático de patinhas, com escala tipográfica ampliada.

#### Scenario: Exibição da identidade visual da Área do Tutor

- **WHEN** a Área do Tutor é exibida
- **THEN** a interface aplica Terracota aberto (`#D9967B` / suave `#F6E9E2`), Sálvia (`#7B9076` / suave `#E7EDE4`) e Soft White (`#FAF8F5`) sobre o fundo `#FFF7ED`
- **AND** renderiza títulos e textos corridos com escala tipográfica ampliada (`size="3"` a `"7"` e `line_height="1.6"`) para maior legibilidade.