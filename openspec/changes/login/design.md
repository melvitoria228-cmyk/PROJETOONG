## Context

O projeto utiliza Reflex no frontend e Xano no backend. A entidade `USUARIO` concentra os dados necessários para o acesso ao sistema, incluindo e-mail, senha e tipo de usuário. A change utilizará essa estrutura para implementar o acesso sem criar uma estrutura paralela de autenticação.

## Goals / Non-Goals

**Goals:**
- Criar uma única interface de login para os usuários do sistema.
- Utilizar o Xano como backend responsável pela autenticação.
- Utilizar o tipo de usuário para diferenciar TUTOR/ADOTANTE e ADMINISTRADOR após o login.
- Manter a solução simples, evitando estruturas de autenticação duplicadas.
- Permitir que a identidade visual da tela seja refinada posteriormente sem alterar a lógica de autenticação.

**Non-Goals:**
- Criar as áreas internas do TUTOR/ADOTANTE ou ADMINISTRADOR.
- Implementar recuperação de senha.
- Implementar cadastro de novos usuários nesta change.
- Criar funcionalidades específicas de adoção ou administração.
- Definir endpoints específicos do Xano neste momento.

## Decisions

### Uma única tela de login

Será utilizada uma única tela para os dois tipos de usuário. O usuário informará e-mail e senha, e o sistema identificará seu tipo de usuário após a autenticação.

**Alternativa considerada:** criar uma tela de login separada para cada tipo de usuário. Essa opção foi descartada para manter o fluxo mais simples e evitar duplicação.

### Reflex como camada de interface

A interface de login será construída utilizando os recursos do Reflex já configurados no projeto.

A implementação deverá separar a apresentação visual da lógica de autenticação, permitindo posteriormente ajustar cores, tipografia, elementos visuais e demais aspectos da identidade da tela sem alterar as regras de autenticação.

**Alternativa considerada:** criar uma página HTML independente. Essa opção não será utilizada porque o frontend definido para o projeto é Reflex.

### Xano como backend de autenticação

A autenticação será realizada pelo backend em Xano. O frontend não deverá manter uma estrutura própria de usuários paralela à entidade `USUARIO`.

**Alternativa considerada:** implementar a autenticação diretamente no frontend. Essa opção foi descartada porque a autenticação deve ser realizada no backend.

### Identificação pelo tipo de usuário

Após uma autenticação válida, o sistema utilizará o `tipo_usuario` associado à conta para identificar se o usuário é TUTOR/ADOTANTE ou ADMINISTRADOR.

O direcionamento para as áreas correspondentes será tratado na implementação da aplicação, respeitando a identificação definida na especificação.

## Risks / Trade-offs

- [Dependência do backend] → A autenticação dependerá da disponibilidade e configuração do Xano.
- [Evolução da interface] → Alterações visuais poderão ocorrer posteriormente sem modificar a lógica de autenticação.
- [Escopo inicial reduzido] → Funcionalidades como recuperação de senha e cadastro não fazem parte desta change e deverão ser tratadas separadamente caso sejam necessárias.

## Migration Plan

Como o Login será uma nova funcionalidade, não há migração de dados prevista nesta change.

A implementação será feita inicialmente no frontend e integrada ao backend conforme a estrutura de autenticação do projeto estiver disponível.

## Open Questions

Nenhuma.
