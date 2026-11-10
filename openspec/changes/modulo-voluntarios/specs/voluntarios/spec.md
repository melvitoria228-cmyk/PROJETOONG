# Capability: Voluntários

## ADDED Requirements

### Requirement: Cadastro de voluntários

O sistema MUST permitir o cadastro dos dados dos voluntários para manter suas informações organizadas.

#### Scenario: Cadastrar voluntário

- WHEN o administrador preencher os dados obrigatórios de um novo voluntário
- THEN o sistema MUST registrar o voluntário.

#### Scenario: Consultar voluntários cadastrados

- WHEN o administrador acessar a área de voluntários
- THEN o sistema MUST apresentar os voluntários cadastrados.

### Requirement: Registro de atividades

O sistema MUST permitir o registro das atividades realizadas pela ONG, mantendo suas informações organizadas.

#### Scenario: Cadastrar atividade

- WHEN o administrador preencher os dados obrigatórios de uma nova atividade
- THEN o sistema MUST registrar a atividade.

#### Scenario: Consultar atividades cadastradas

- WHEN o administrador acessar a área de atividades
- THEN o sistema MUST apresentar as atividades cadastradas.

### Requirement: Associação entre voluntários e atividades

O sistema MUST permitir associar voluntários às atividades das quais participam.

#### Scenario: Associar voluntário a uma atividade

- WHEN o administrador selecionar um voluntário e uma atividade
- THEN o sistema MUST registrar a participação do voluntário naquela atividade.

#### Scenario: Atividade com vários voluntários

- WHEN vários voluntários participarem da mesma atividade
- THEN o sistema MUST permitir associar todos eles à atividade.

#### Scenario: Voluntário participa de várias atividades

- WHEN um voluntário participar de diferentes atividades
- THEN o sistema MUST permitir registrar cada participação de forma independente.

### Requirement: Histórico de participação

O sistema MUST manter o histórico das atividades das quais cada voluntário participou.

#### Scenario: Consultar histórico de um voluntário

- WHEN o administrador consultar o histórico de um voluntário
- THEN o sistema MUST apresentar as atividades associadas a ele.

#### Scenario: Consultar participantes de uma atividade

- WHEN o administrador consultar uma atividade
- THEN o sistema MUST apresentar os voluntários associados a ela.
