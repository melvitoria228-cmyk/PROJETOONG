## 1. Conferir a estrutura existente

* [x] 1.1 Inspecionar a implementação atual de `ProjetoONG.py` e identificar os padrões utilizados na área administrativa, sem alterar o arquivo.
* [x] 1.2 Conferir os endpoints existentes da tabela `ANIMAL` no Xano.
* [x] 1.3 Confirmar os campos, tipos, obrigatoriedade e valores aceitos pelo Xano.

## 2. Preparar a integração com o Xano

* [x] 2.1 Reutilizar a configuração de conexão existente no projeto.
* [x] 2.2 Implementar as operações de consulta, cadastro, edição e exclusão usando os endpoints existentes.
* [x] 2.3 Tratar erros do Xano sem apresentar operações malsucedidas como concluídas.

## 3. Implementar a consulta de animais

* [x] 3.1 Criar a tela de Gestão de Animais na área administrativa, seguindo a estrutura e o design existentes.
* [x] 3.2 Exibir os animais retornados pelo Xano, incluindo seus status, com estados de carregamento, lista vazia e erro.
* [x] 3.3 Permitir consultar os detalhes de um animal selecionado.

## 4. Implementar cadastro e edição

* [x] 4.1 Criar o formulário de cadastro com os campos e as opções confirmados no Xano.
* [x] 4.2 Validar os campos obrigatórios antes do envio.
* [x] 4.3 Implementar o cadastro e atualizar a lista somente após a confirmação de sucesso do Xano.
* [x] 4.4 Implementar a edição de animais existentes e atualizar a lista somente após a confirmação de sucesso do Xano.

## 5. Implementar exclusão e identidade visual

* [x] 5.1 Implementar a exclusão com confirmação explícita e tratar tanto o sucesso quanto a falha da operação.
* [x] 5.2 Aplicar a paleta administrativa definida no design e indicadores visuais de status acompanhados de texto legível.

## 6. Validar a implementação

* [x] 6.1 Testar consulta, cadastro, edição e exclusão, incluindo validações, falhas de comunicação e situações em que a exclusão não é permitida.
* [x] 6.2 Executar a validação do OpenSpec e verificar se o login, as rotas administrativas e a área do tutor/adotante continuam funcionando.
