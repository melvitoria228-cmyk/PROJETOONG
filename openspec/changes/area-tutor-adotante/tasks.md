## 1. Preparação e validação

- [x] 1.1 Conferir os requisitos e o design da mudança.
- [x] 1.2 Executar `openspec validate --changes area-tutor-adotante` e confirmar que não há falhas.
- [x] 1.3 Conferir a implementação atual do login e o registro das páginas em `ProjetoONG/ProjetoONG.py`.

## 2. Implementação da página inicial

- [x] 2.1 Criar a função da página inicial do Tutor/Adotante em `ProjetoONG/ProjetoONG.py`.
- [x] 2.2 Criar um cabeçalho superior com a marca Porto Seguro Pet e a identificação “Área do Tutor/Adotante”.
- [x] 2.3 Criar uma área de boas-vindas com mensagem acolhedora.
- [x] 2.4 Criar os quatro cartões: “Minhas adoções”, “Acompanhamento”, “Meus dados” e “Orientações”.
- [x] 2.5 Aplicar a paleta grafite `#3E4149`, creme `#F4E7D5` e terracota `#D78A45`.
- [x] 2.6 Registrar a página na rota `/tutor`.
- [x] 2.7 Conferir a apresentação inicial dos cartões.

## 3. Autenticação e redirecionamento

- [x] 3.1 Verificar o redirecionamento de usuários autenticados do tipo `administrador` para `/administrativo`.
- [x] 3.2 Verificar o redirecionamento de usuários autenticados do tipo `tutor/adotante` para `/tutor`.
- [ ] 3.3 Verificar que um tipo de usuário desconhecido não recebe redirecionamento para uma área restrita.
- [x] 3.4 Executar a aplicação e testar a abertura da rota `/tutor` no navegador.

## 4. Consulta dos processos de adoção

- [x] 4.1 Configurar a consulta dos processos de adoção por meio do endpoint GET do Xano.
- [x] 4.2 Utilizar o token de autenticação na consulta.
- [x] 4.3 Testar a consulta e confirmar o recebimento de dados reais do backend.
- [ ] 4.4 Melhorar a apresentação dos dados, explicando o significado dos campos exibidos.
- [ ] 4.5 Verificar como identificar o animal relacionado a cada processo, incluindo nome e espécie quando disponíveis.
- [ ] 4.6 Verificar a disponibilidade de fotos dos animais e a necessidade de um endpoint adicional.
- [ ] 4.7 Testar a apresentação dos dados com processos reais e com a ausência de resultados.

## 5. Navegação pelos cartões

- [x] 5.1 Tornar o cartão “Minhas adoções” acessível por meio de sua página específica.
- [x] 5.2 Tornar o cartão “Acompanhamento” acessível por meio de sua página específica.
- [x] 5.3 Tornar o cartão “Meus dados” acessível por meio de sua página específica.
- [x] 5.4 Tornar o cartão “Orientações” acessível por meio de sua página específica.
- [x] 5.5 Testar a navegação e o retorno à página inicial.

## 6. Acompanhamento pós-adoção

- [x] 6.1 Conferir a estrutura da tabela de acompanhamento pós-adoção no Xano.
- [x] 6.2 Configurar os endpoints necessários para consultar os registros de acompanhamento.
- [x] 6.3 Criar a página de acompanhamento pós-adoção.
- [x] 6.4 Exibir os registros relacionados às adoções do tutor autenticado.
- [ ] 6.5 Testar a consulta, os casos sem registros e as permissões de acesso.

## 7. Meus dados e Orientações

- [x] 7.1 Verificar quais dados do tutor estão disponíveis no endpoint de autenticação ou em outros endpoints existentes.
- [x] 7.2 Criar a página “Meus dados” utilizando as informações disponíveis.
- [x] 7.3 Definir o conteúdo informativo da página “Orientações”.
- [x] 7.4 Criar a página “Orientações” sem adicionar funcionalidades desnecessárias.
- [x] 7.5 Testar as duas páginas e sua navegação.

## 8. Validação final

- [x] 8.1 Testar o fluxo de login e os redirecionamentos.
- [x] 8.2 Testar a navegação pelos cartões e suas respectivas páginas.
- [ ] 8.3 Conferir a apresentação dos dados de adoção e o tratamento de erros.
- [x] 8.4 Conferir a identidade visual e a consistência das páginas.
- [ ] 8.5 Verificar as permissões de acesso aos dados no backend.
- [ ] 8.6 Executar `openspec validate --changes area-tutor-adotante` e confirmar que a documentação continua válida.
