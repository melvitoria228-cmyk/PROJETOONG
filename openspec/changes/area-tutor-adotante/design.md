# Design: Área do Tutor/Adotante

## Context

O frontend do sistema Porto Seguro Pet utiliza Reflex, com o Xano como backend. A aplicação possui uma página de login, uma área administrativa registrada na rota `/administrativo` e uma área do Tutor/Adotante registrada na rota `/tutor`.

A autenticação consulta o Xano para validar o usuário e identificar seu tipo de acesso. Após o login, o usuário é redirecionado para a área correspondente ao seu perfil.

A área do Tutor/Adotante possui um cabeçalho, uma mensagem de boas-vindas e quatro cartões: “Minhas adoções”, “Acompanhamento”, “Meus dados” e “Orientações”.

A funcionalidade “Minhas adoções” já possui uma página própria e consulta os processos de adoção por meio de um endpoint GET do Xano, utilizando o token de autenticação. A interface apresenta informações retornadas pelo backend, incluindo o status do processo, a data da solicitação e o identificador do animal.

Apesar de a consulta estar funcionando, sua apresentação visual ainda precisa ser aprimorada. Pretende-se tornar as informações mais dinâmicas, organizadas e fáceis de compreender, explicando o significado dos campos e facilitando a identificação do animal relacionado a cada processo.

Os demais cartões serão implementados gradualmente. O cartão “Acompanhamento” dependerá da integração com os registros de acompanhamento pós-adoção. O cartão “Meus dados” poderá utilizar as informações do usuário disponíveis no backend, enquanto “Orientações” poderá apresentar conteúdo informativo estático.

Os requisitos funcionais desta mudança estão definidos em `specs/area-tutor-adotante/spec.md`.

## Goals / Non-Goals

### Goals

- Manter uma página inicial organizada para o Tutor/Adotante.
- Disponibilizar a página na rota `/tutor`.
- Manter o cabeçalho superior, a área de boas-vindas e os quatro cartões.
- Aplicar a paleta de cores grafite, creme e terracota.
- Permitir a navegação dos cartões para páginas específicas conforme suas funcionalidades forem implementadas.
- Consultar e exibir os processos de adoção reais retornados pelo Xano.
- Utilizar o token de autenticação nas requisições que exigem acesso autenticado.
- Reutilizar componentes e funções existentes para manter o código simples e organizado.
- Preparar a navegação para a futura integração do acompanhamento pós-adoção.
- Melhorar a apresentação visual da página “Minhas adoções”, tornando a consulta mais dinâmica, organizada e fácil de compreender.
- Explicar o significado dos campos apresentados na consulta, utilizando rótulos claros e descrições simples quando necessário.
- Facilitar a identificação do animal relacionado a cada processo, evitando que o tutor precise reconhecê-lo apenas pelo identificador numérico.
- Organizar as informações para que o tutor compreenda rapidamente a situação e o andamento de sua solicitação de adoção.

### Non-Goals

- Implementar funcionalidades que não estejam previstas nos requisitos do projeto.
- Criar uma nova tabela no banco apenas para representar um cartão da interface.
- Implementar o acompanhamento pós-adoção antes de configurar e validar seus endpoints.
- Implementar edição de dados pessoais sem verificar previamente os endpoints disponíveis.
- Substituir a autenticação existente ou introduzir novas dependências desnecessárias.
- Considerar a autorização das operações garantida apenas porque o usuário está autenticado no frontend.
- Alterar desnecessariamente a estrutura do banco para melhorar a apresentação visual da consulta.
- Exibir fotografias ou informações de animais que não estejam disponíveis ou não possam ser obtidas de forma confiável no backend.

## Decisions

- **Manter Reflex:** utilizar a tecnologia já adotada no frontend.
- **Manter o Xano como backend:** realizar as consultas e operações necessárias por meio dos endpoints existentes.
- **Separar as páginas:** manter a área administrativa, a área do Tutor/Adotante e as páginas de funcionalidades em rotas próprias.
- **Manter a rota `/tutor`:** utilizar a rota já registrada para a área inicial do Tutor/Adotante.
- **Reutilizar o componente `cartao_tutor`:** centralizar a apresentação visual dos cartões e permitir a definição de uma rota de destino para cada um.
- **Manter os quatro cartões:** “Minhas adoções”, “Acompanhamento”, “Meus dados” e “Orientações”.
- **Consultar os processos de adoção pelo Xano:** utilizar o endpoint GET já configurado, enviando o token de autenticação quando necessário.
- **Exibir dados reais:** apresentar as informações efetivamente retornadas pelo backend, sem simular processos de adoção.
- **Separar interface e dados:** um cartão representa uma opção de navegação e não precisa corresponder diretamente a uma tabela do banco.
- **Implementar gradualmente os cartões:** priorizar as funcionalidades já iniciadas e configurar os endpoints necessários antes de integrar novas consultas.
- **Melhorar a consulta de adoções:** reformular gradualmente a apresentação da página “Minhas adoções”, priorizando a clareza das informações e a facilidade de uso.
- **Utilizar rótulos explicativos:** apresentar nomes compreensíveis para os campos e descrições simples quando necessário. Por exemplo, explicar que o status representa a situação atual do processo de adoção.
- **Identificar visualmente o animal:** verificar quais informações estão disponíveis para apresentar o animal associado a cada processo, como nome, espécie e, se houver, fotografia.
- **Preservar os dados do backend:** manter a consulta baseada nos dados reais retornados pelo Xano, melhorando sua apresentação no frontend sem inventar informações.
- **Priorizar a compreensão do tutor:** organizar os dados em cartões, seções ou outros elementos visuais adequados, evitando a exibição de identificadores técnicos sem explicação.
- **Verificar a disponibilidade dos dados:** antes de implementar a identificação visual do animal, conferir se o endpoint de adoções retorna informações suficientes ou se será necessário consultar outro endpoint.
- **Manter a identidade visual:** utilizar grafite `#3E4149`, creme `#F4E7D5` e terracota `#D78A45`, com fundos claros, cantos arredondados e espaçamento confortável.

## Risks / Trade-offs

- **Rotas incorretas:** verificar se cada cartão direciona para a página esperada.
- **Endpoints indisponíveis ou incorretos:** testar as URLs, os métodos HTTP e os formatos das respostas do Xano.
- **Falhas de autenticação:** tratar respostas de erro e verificar se o token é enviado corretamente.
- **Exposição ou alteração indevida de dados:** verificar no backend se cada usuário só pode consultar ou alterar os registros aos quais tem permissão.
- **Funcionalidades parcialmente implementadas:** distinguir os cartões que já possuem páginas funcionais daqueles que ainda dependem de implementação.
- **Dependência de novos endpoints:** o acompanhamento pós-adoção precisará de consultas próprias, conforme a estrutura da tabela e os requisitos definidos.
- **Identificação incompleta do animal:** o endpoint de adoções pode retornar apenas o identificador do animal, exigindo uma consulta adicional para obter seu nome, espécie ou fotografia.
- **Excesso de informações na consulta:** adicionar explicações e elementos visuais sem comprometer a organização e a simplicidade da interface.
- **Complexidade desnecessária:** priorizar o reaproveitamento de componentes e endpoints existentes, evitando duplicações.

## Migration Plan

1. Atualizar a documentação OpenSpec para refletir a implementação atual.
2. Manter a página do Tutor/Adotante registrada na rota `/tutor`.
3. Manter o redirecionamento após o login conforme o tipo de usuário.
4. Manter a página “Minhas adoções” integrada ao endpoint GET do Xano.
5. Testar a exibição do status, da data da solicitação e do identificador do animal.
6. Tornar os cartões restantes clicáveis e definir suas páginas de destino.
7. Configurar e testar os endpoints necessários para o acompanhamento pós-adoção.
8. Verificar quais dados e endpoints existentes podem ser utilizados em “Meus dados”.
9. Criar a página de “Orientações” com conteúdo informativo, sem exigir endpoint quando não houver necessidade.
10. Testar as rotas, o comportamento dos cartões e as respostas da API.
11. Atualizar os requisitos e as tarefas do OpenSpec conforme o avanço real da implementação.
12. Executar a validação do OpenSpec e corrigir inconsistências antes de considerar a mudança concluída.
13. Revisar a apresentação atual da página “Minhas adoções” e identificar os campos que precisam de explicações.
14. Verificar quais informações do animal relacionado ao processo estão disponíveis no Xano e se é necessário consultar outro endpoint.
15. Reformular a interface para destacar o animal, explicar os campos e facilitar a compreensão do status do processo.
16. Testar a nova apresentação com os dados reais retornados pelo backend.
