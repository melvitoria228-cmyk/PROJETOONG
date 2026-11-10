# Design: Módulo de Voluntários

## Context

O módulo de Voluntários fará parte da área administrativa do Porto Seguro Pet. Seu objetivo é organizar os dados dos voluntários e registrar as atividades das quais participam.

A interface será desenvolvida em Python com Reflex. A integração com o banco de dados Xano será realizada posteriormente.

## Goals / Non-Goals

### Goals

- Disponibilizar uma interface administrativa para o gerenciamento de voluntários.
- Permitir o cadastro e a consulta de voluntários.
- Permitir o registro e a consulta de atividades.
- Associar voluntários às atividades realizadas.
- Manter o histórico de participação dos voluntários.

### Non-Goals

- Implementar controle de pagamentos ou remuneração.
- Gerenciar escalas complexas de trabalho.
- Implementar controle de ponto ou frequência.
- Gerenciar folha de pagamento.
- Implementar funcionalidades de recrutamento ou seleção.

## Decisions

### 1. Organização da interface

A interface será acessada pelo menu administrativo por meio da opção Voluntários.

O módulo será organizado em áreas para:
- Consulta e cadastro de voluntários.
- Registro e consulta de atividades.
- Consulta do histórico de participação.

### 2. Cadastro de voluntários

O sistema permitirá cadastrar e consultar os dados dos voluntários, mantendo suas informações organizadas.

### 3. Registro de atividades

O sistema permitirá registrar as atividades realizadas pelos voluntários e consultar os respectivos registros.

### 4. Associação entre voluntários e atividades

Um voluntário poderá participar de várias atividades, e uma atividade poderá contar com a participação de vários voluntários.

A entidade VOLUNTARIO_ATIVIDADE será utilizada para representar essa associação.

### 5. Organização dos dados

Serão utilizadas as entidades VOLUNTARIO, ATIVIDADE e VOLUNTARIO_ATIVIDADE, conforme o modelo de dados do projeto.

### 6. Integração com o banco de dados

Inicialmente, a interface será desenvolvida sem integração com o Xano. A conectividade será implementada em uma etapa posterior.

## Risks / Trade-offs

- Os registros de participação dependerão da associação correta entre voluntários e atividades.
- A ausência de controle de ponto significa que o módulo não calculará horas trabalhadas ou frequência dos voluntários.

## Migration Plan

1. Criar a interface administrativa de Voluntários.
2. Criar a estrutura de estado do módulo.
3. Implementar os componentes de cadastro, registro e consulta.
4. Registrar a rota e integrar a opção ao menu administrativo.
5. Realizar a integração com o Xano posteriormente.
