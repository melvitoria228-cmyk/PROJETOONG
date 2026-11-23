## 1. Preparação e validação

- [x] 1.1 Conferir os requisitos e o design da mudança.
- [x] 1.2 Executar `openspec validate --changes area-tutor-adotante` e confirmar que não há falhas.
- [x] 1.3 Conferir a implementação atual do login, estados e registro das páginas em `ProjetoONG/ProjetoONG.py`.

## 2. Implementação da interface unificada (`/tutor`)

- [x] 2.1 Refatorar a função da página inicial do Tutor/Adotante (`area_tutor`) em `ProjetoONG/ProjetoONG.py`.
- [x] 2.2 Criar a barra superior fixa com a marca Porto Seguro Pet, saudação personalizada ao tutor logado e botão de encerramento de sessão (`LoginState.sair`).
- [x] 2.3 Estruturar a navegação centralizada por **3 abas** (`aba_tutor_ativa`): *Minhas Adoções*, *Pós-Adoção e Guias* e *Meu Perfil*.
- [x] 2.4 Aplicar a nova paleta acolhedora da Área do Tutor: Terracota aberto (`#D9967B` / suave `#F6E9E2`), Sálvia (`#7B9076` / suave `#E7EDE4`) e Soft White (`#FAF8F5`) sobre o fundo temático com patinhas (`#FFF7ED`).
- [x] 2.5 Aplicar a escala tipográfica ampliada (`size="3"` a `"7"` e `line_height="1.6"`) para maior conforto de leitura.
- [x] 2.6 Registrar a rota `/tutor` com disparo automático de `LoginState.iniciar_painel_tutor` no ciclo `on_load`.

## 3. Autenticação, redirecionamento e compatibilidade de rotas

- [x] 3.1 Verificar o redirecionamento de usuários autenticados do tipo `administrador` para `/administrativo`.
- [x] 3.2 Verificar o redirecionamento de usuários autenticados do tipo `tutor/adotante` para `/tutor`.
- [x] 3.3 Verificar que um tipo de usuário desconhecido não recebe redirecionamento para área restrita e exibe mensagem de alerta.
- [x] 3.4 Configurar as rotas anteriores (`/acompanhamento`, `/meus-dados`, `/orientacoes`) para redirecionar para `/tutor` ativando automaticamente a aba correspondente.

## 4. Aba Minhas Adoções (`aba_minhas_adocoes_tutor`)

- [x] 4.1 Configurar a consulta autenticada (`GET` com token JWT) dos processos de adoção vinculados ao tutor no Xano.
- [x] 4.2 Garantir o carregamento automático das solicitações ao entrar no painel `/tutor` via `iniciar_painel_tutor`.
- [x] 4.3 Utilizar os dados retornados pelo Add-on `_animal` no Xano para exibir o nome real do animal no cabeçalho de cada cartão (com fallback seguro caso ausente).
- [x] 4.4 Implementar o indicador visual de progresso por etapas (**1. Análise**, **2. Aprovação**, **3. Conclusão**) e as caixas explicativas correspondentes a cada status.
- [x] 4.5 Tratar estados de carregamento, ausência de solicitações (estado vazio) e falhas de conexão com feedback via `rx.toast`.

## 5. Aba Pós-Adoção e Guias (`aba_pos_adocao_e_guias_tutor`)

- [x] 5.1 Configurar o endpoint `XANO_ACOMPANHAMENTO_LIST_URL` e o carregamento automático dos registros de acompanhamento pós-adoção do tutor.
- [x] 5.2 Exibir o histórico de visitas, datas e observações registradas pela equipe da ONG, tratando estados vazios e erros de consulta.
- [x] 5.3 Construir os guias educativos de guarda responsável (adaptação, saúde, vacinação e segurança) utilizando cartões nativos do Reflex (`card_guia_tutor`), eliminando dependências externas conflitantes.

## 6. Aba Meu Perfil (`aba_meu_perfil_tutor`)

- [x] 6.1 Capturar e preencher automaticamente os dados do tutor cadastrado (`id`, `nome`, `cpf`, `telefone`, `tipo_residencia`, `endereco`) a partir da resposta da API Xano no login.
- [x] 6.2 Criar o formulário integrado de consulta e edição cadastral diretamente na aba *Meu Perfil*.
- [x] 6.3 Conectar o botão "Salvar Alterações" ao endpoint `PATCH /tutor_adotante` do Xano com token JWT e feedback visual via `rx.toast`.

## 7. Validação final

- [x] 7.1 Testar o fluxo de login, o logout e os redirecionamentos por perfil e rotas de compatibilidade.
- [x] 7.2 Testar a navegação entre as 3 abas (*Minhas Adoções*, *Pós-Adoção e Guias* e *Meu Perfil*) e o carregamento automático inicial.
- [x] 7.3 Conferir a exibição do nome real do pet, o indicador de progresso em 3 etapas e os cartões nativos de orientações.
- [x] 7.4 Conferir a identidade visual (Terracota aberto, Sálvia e Soft White) e a legibilidade da tipografia ampliada.
- [x] 7.5 Verificar a persistência das alterações cadastrais no backend Xano e executar `openspec validate --changes area-tutor-adotante`.