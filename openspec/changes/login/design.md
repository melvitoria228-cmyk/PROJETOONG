# Design: Login

## Context

O projeto utiliza Reflex no frontend e Xano no backend[cite: 1]. A entidade `USUARIO` concentra os dados necessários para o acesso ao sistema, incluindo e-mail, senha e tipo de usuário[cite: 19]. A change utiliza essa estrutura para implementar o acesso e direcionamento sem criar uma estrutura paralela de autenticação[cite: 1, 16].

## Goals 

**Goals:**
- Criar uma única interface de login para os usuários do sistema[cite: 1].
- Exibir um carrossel visual automático com fotos de animais na lateral da tela de login para enriquecer a experiência do usuário[cite: 1].
- Utilizar o Xano como backend responsável pela autenticação[cite: 1].
- Utilizar o tipo de usuário para diferenciar TUTOR/ADOTANTE e ADMINISTRADOR e direcionar para suas respectivas áreas após o login[cite: 1].
- Manter a solução simples, utilizando o estado global do Reflex (`LoginState`)[cite: 1].
- Disponibilizar interfaces visuais de suporte (recuperação e alteração de senha) com avisos orientativos[cite: 1].

## Non-Goals:
- Implementar a lógica de backend completa para envio de e-mails de recuperação de senha nesta change[cite: 1].
- Implementar formulário de auto-cadastro de novos usuários nesta change.
- Criar funcionalidades específicas de adoção ou administração na tela de login.

## Decisions

### Uma única tela de login com carrossel visual

Será utilizada uma única tela para os dois tipos de usuário. A interface é dividida em duas colunas: a esquerda apresenta um carrossel automático de imagens de animais com animação e a direita contém o formulário de login (`email` e `senha`) com fundo personalizado[cite: 1].

### Carrossel automático no Reflex

O carrossel utiliza imagens de animais configuradas no estado (`fotos_carrossel`), com transição automática por tempo via evento assíncrono em segundo plano (`iniciar_carrossel_automatico`), além de suporte à navegação[cite: 1].

### Xano como backend de autenticação

A autenticação é realizada pelo backend em Xano via requisição `POST` no endpoint de login[cite: 1]. O token retornado é utilizado na consulta do usuário (`GET /auth/me`) para identificar o `tipo_usuario` e o vínculo com a tabela `TUTOR_ADOTANTE`[cite: 1].

### Identificação e direcionamento pelo tipo de usuário

Após uma autenticação válida, o sistema utiliza o `tipo_usuario` para redirecionar o usuário:
- `administrador` → redirecionado para a rota `/administrativo`[cite: 1].
- `tutor/adotante` → redirecionado para a rota `/tutor`[cite: 1].

## Risks / Trade-offs

- [Dependência do backend] → A autenticação depende da disponibilidade e configuração dos endpoints do Xano (`XANO_LOGIN_URL` e `XANO_ME_URL`)[cite: 1].
- [Imagens externas do carrossel] → O carrossel depende do carregamento de URLs de imagens[cite: 1].
- [Escopo de recuperação de senha] → As telas de alteração e recuperação de senha funcionam no nível visual/simulado com feedback por `rx.toast` até a futura integração dos endpoints[cite: 1].

## Migration Plan

Como o Login é a porta de entrada da aplicação, a página está registrada e ativa na rota principal `/`[cite: 1].

A implementação já se encontra integrada com o backend Xano e direciona corretamente para `/administrativo` e `/tutor`[cite: 1].

## Open Questions

Nenhuma.