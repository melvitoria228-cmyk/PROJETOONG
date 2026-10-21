## Why

O sistema precisa oferecer uma área inicial própria para tutores e adotantes, permitindo que o login encaminhe cada usuário para a página correspondente ao seu tipo de acesso. Essa área deve facilitar a navegação pelas funcionalidades disponíveis e permitir que o tutor consulte informações sobre seus processos de adoção de maneira clara e organizada.

## What Changes

- Manter uma página inicial para Tutor/Adotante na rota `/tutor`.
- Exibir uma identificação clara da área, uma mensagem de boas-vindas e os cartões de navegação.
- Disponibilizar os cartões “Minhas adoções”, “Acompanhamento”, “Meus dados” e “Orientações” como opções de acesso às respectivas páginas.
- Manter a consulta dos processos de adoção integrada ao Xano, utilizando os dados reais retornados pelo backend.
- Planejar melhorias na apresentação da consulta de adoções, incluindo explicações dos campos e identificação mais clara do animal relacionado a cada processo.
- Implementar gradualmente as funcionalidades dos cartões, respeitando o escopo definido para cada uma.
- Preservar a autenticação e o redirecionamento conforme o tipo de usuário.

## Capabilities

### New Capabilities

- `area-tutor-adotante`: define o comportamento, a apresentação e a navegação da área de Tutor/Adotante, incluindo a consulta dos processos de adoção.

### Modified Capabilities

- Nenhuma.

## Impact

- **Frontend Reflex:** manutenção da página inicial, organização das páginas e implementação gradual da navegação pelos cartões.
- **Login:** manutenção da integração entre a autenticação e o redirecionamento para a área correspondente ao tipo de usuário.
- **Backend Xano:** utilização dos endpoints existentes para consultar os processos de adoção e possível necessidade de consultas adicionais para obter informações completas dos animais.
- **Acompanhamento pós-adoção:** configuração futura dos endpoints necessários para consultar os registros correspondentes.
- **Documentação OpenSpec:** atualização dos requisitos e das tarefas para refletir as funcionalidades implementadas e as melhorias planejadas.
