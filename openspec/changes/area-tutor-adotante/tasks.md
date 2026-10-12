## 1. Preparação e validação

* [x] 1.1 Conferir os requisitos e o design da mudança.
* [x] 1.2 Executar `openspec validate --changes area-tutor-adotante` e confirmar que não há falhas.
* [x] 1.3 Conferir a implementação atual do login e o registro das páginas em `ProjetoONG/ProjetoONG.py`.

## 2. Implementação da página

* [x] 2.1 Criar a função da página inicial do Tutor/Adotante em `ProjetoONG/ProjetoONG.py`.
* [x] 2.2 Criar um cabeçalho superior com a marca Porto Seguro Pet e a identificação “Área do Tutor/Adotante”.
* [x] 2.3 Criar uma área de boas-vindas com mensagem acolhedora.
* [x] 2.4 Criar os quatro cartões visuais: “Minhas adoções”, “Acompanhamento”, “Meus dados” e “Orientações”.
* [x] 2.5 Aplicar a paleta grafite `#3E4149`, creme `#F4E7D5` e terracota `#D78A45`.
* [x] 2.6 Registrar a página na rota `/tutor`.
* [x] 2.7 Verificar que os cartões não apresentam funcionalidades como se já estivessem implementadas.

## 3. Integração e testes

* [x] 3.1 Verificar que o login direciona um usuário autenticado do tipo `administrador` para `/administrativo`.
* [x] 3.2 Verificar que o login direciona um usuário autenticado do tipo `tutor/adotante` para `/tutor`.
* [ ] 3.3 Verificar que um tipo de usuário desconhecido não recebe redirecionamento para uma área restrita.
* [x] 3.4 Executar a aplicação e testar a abertura da rota `/tutor` no navegador.
* [x] 3.5 Conferir o cabeçalho, a mensagem de boas-vindas, os quatro cartões e as cores.
* [x] 3.6 Executar `openspec validate --changes area-tutor-adotante` e confirmar que a documentação continua válida.
