# Spec: Módulo de Voluntários

## Purpose

Definir os requisitos funcionais do módulo administrativo de **Voluntários** na rota `/voluntarios`, permitindo cadastrar e consultar voluntários (`VOLUNTARIO`), registrar atividades da ONG (`ATIVIDADE`), associar participações (`VOLUNTARIO_ATIVIDADE`) sem duplicidade e consultar o histórico bidirecional integrado ao backend Xano.

## ADDED Requirements

### Requirement: Carregamento Automático e Indicadores de Voluntariado

O sistema MUST carregar automaticamente os registros de voluntários, atividades e participações no `on_load` da rota `/voluntarios` (via token JWT do Xano) e exibir indicadores resumidos do módulo.

#### Scenario: Carregar painel de voluntários com sucesso
- **WHEN** o administrador acessar a rota `/voluntarios`
- **THEN** o sistema MUST consultar os registros autenticados de `VOLUNTARIO`, `ATIVIDADE` e `VOLUNTARIO_ATIVIDADE` no Xano, exibir os indicadores resumidos (total de voluntários, total de atividades e total de participações) e apresentar as listagens na interface.

#### Scenario: Falha de comunicação com o backend
- **WHEN** ocorrer erro de rede ou rejeição na consulta ou gravação junto ao Xano
- **THEN** o sistema MUST preservar o estado atual da interface e notificar o usuário via *toast*.

### Requirement: Cadastro e Consulta de Voluntários

O sistema MUST permitir o cadastro (`POST`) e a consulta (`GET`) dos dados dos voluntários (`VOLUNTARIO`) integrados ao Xano.

#### Scenario: Cadastrar novo voluntário
- **WHEN** o administrador preencher os dados obrigatórios de um novo voluntário e confirmar o envio
- **THEN** o sistema MUST registrar o voluntário no Xano, atualizar a listagem disponível para associação em atividades e exibir confirmação via *toast*.

#### Scenario: Consultar e filtrar voluntários cadastrados
- **WHEN** o administrador acessar a área de voluntários ou aplicar filtro de pesquisa por nome, disponibilidade ou habilidade
- **THEN** o sistema MUST apresentar os voluntários correspondentes com suas informações organizadas.

### Requirement: Registro e Consulta de Atividades

O sistema MUST permitir o registro (`POST`) e a consulta (`GET`) das atividades realizadas pela ONG (`ATIVIDADE`).

#### Scenario: Cadastrar nova atividade
- **WHEN** o administrador preencher os dados obrigatórios de uma nova atividade (título, data e descrição/local) e confirmar o envio
- **THEN** o sistema MUST registrar a atividade no Xano, atualizar a listagem e exibir confirmação via *toast*.

#### Scenario: Consultar atividades cadastradas
- **WHEN** o administrador acessar a área de atividades
- **THEN** o sistema MUST apresentar as atividades cadastradas com data, descrição e quantidade de participantes vinculados.

### Requirement: Associação entre Voluntários e Atividades

O sistema MUST permitir associar voluntários às atividades (`POST` em `VOLUNTARIO_ATIVIDADE`), suportando relacionamento `N:N` e prevenindo vínculos duplicados.

#### Scenario: Associar voluntário a uma atividade
- **WHEN** o administrador selecionar um voluntário e uma atividade ainda não vinculados e confirmar a associação
- **THEN** o sistema MUST registrar a participação na entidade `VOLUNTARIO_ATIVIDADE` no Xano e exibir confirmação via *toast*.

#### Scenario: Impedir associação duplicada na mesma atividade
- **WHEN** o administrador tentar associar um voluntário que já esteja vinculado à mesma atividade
- **THEN** o sistema MUST impedir o registro duplicado e exibir alerta orientativo via *toast*.

#### Scenario: Relacionamento múltiplo entre voluntários e atividades
- **WHEN** vários voluntários participarem da mesma atividade ou um voluntário participar de diferentes atividades ao longo do tempo
- **THEN** o sistema MUST registrar e manter cada vínculo de participação de forma independente em `VOLUNTARIO_ATIVIDADE`.

### Requirement: Histórico Bidirecional de Participação

O sistema MUST manter e exibir o histórico das atividades de cada voluntário e dos voluntários participantes de cada atividade.

#### Scenario: Consultar histórico de um voluntário
- **WHEN** o administrador consultar ou filtrar o histórico por um voluntário específico
- **THEN** o sistema MUST apresentar todas as atividades associadas àquele voluntário.

#### Scenario: Consultar participantes de uma atividade
- **WHEN** o administrador consultar ou filtrar uma atividade específica
- **THEN** o sistema MUST apresentar todos os voluntários associados àquela atividade.