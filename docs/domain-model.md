## 1. Visão do domínio
O domínio do **Porto Seguro Pet** representa os processos operacionais e administrativos de uma ONG de proteção animal, abrangendo o gerenciamento dos animais desde o resgate até a adoção responsável e o acompanhamento pós-adoção, além da gestão de tutores/adotantes, lares temporários, atendimentos veterinários, voluntários, atividades, doadores e doações (financeiras e materiais).

## 2. Principais conceitos do domínio
1. **Animal (`ANIMAL`):** representa os animais resgatados e atendidos pela ONG, incluindo suas características físicas, condição clínica, alergias, restrições e status atual (`Disponível`, `Em Lar Temporário`, `Em Processo de Adoção`, `Adotado` ou `Falecido`).
2. **Lar Temporário (`LAR_TEMPORARIO`):** representa os locais parceiros onde os animais podem permanecer acolhidos temporariamente.
3. **Permanência em Lar Temporário (`ANIMAL_LAR_TEMPORARIO`):** representa o histórico de acolhimento de cada animal nos lares temporários, com datas de entrada e saída.
4. **Atendimento Veterinário (`ATENDIMENTO_VETERINARIO`):** representa os agendamentos, avaliações clínicas, procedimentos, tratamentos e custos veterinários realizados nos animais.
5. **Tutor/Adotante (`TUTOR_ADOTANTE`):** representa a pessoa cadastrada (com CPF único) que utiliza o sistema para solicitar e acompanhar processos de adoção.
6. **Usuário (`USUARIO`):** representa a conta de acesso ao sistema (e-mail único e senha), podendo estar associada a um `TUTOR/ADOTANTE` ou possuir perfil `ADMINISTRADOR`.
7. **Processo de Adoção (`PROCESSO_ADOCAO`):** representa a solicitação, triagem, aprovação/recusa e efetivação da adoção de um animal por um tutor/adotante.
8. **Acompanhamento Pós-Adoção (`ACOMPANHAMENTO_POS_ADOCAO`):** representa os registros cronológicos de acompanhamento realizados após a efetivação da adoção.
9. **Voluntário (`VOLUNTARIO`):** representa as pessoas aprovadas para atuar nas ações e atividades da ONG.
10. **Atividade (`ATIVIDADE`):** representa as ações operacionais e eventos organizados pela ONG com participação de voluntários.
11. **Participação em Atividade (`VOLUNTARIO_ATIVIDADE`):** representa o vínculo de atuação de um voluntário em determinada atividade, incluindo a função exercida.
12. **Doador (`DOADOR`):** representa o cadastro único (CPF único quando informado) de quem realiza contribuições financeiras ou materiais para a ONG.
13. **Doação (`DOACAO`):** representa as contribuições financeiras (valor e data) e materiais (descrição dos itens e data) recebidas pela ONG, sem controle de movimentação de estoque.

## 3. Relacionamentos do domínio
1. **Animal (1) : (N) Lar Temporário (via `ANIMAL_LAR_TEMPORARIO`):** um animal pode possuir vários registros históricos de acolhimento em lares temporários.
2. **Animal (1) : (N) Atendimento Veterinário:** um animal pode possuir vários registros de atendimentos veterinários ao longo do tempo.
3. **Animal (1) : (N) Processo de Adoção:** um animal pode estar vinculado a diferentes solicitações/processos de adoção até sua efetivação.
4. **Tutor/Adotante (1) : (N) Processo de Adoção:** um tutor/adotante pode realizar várias solicitações de adoção.
5. **Processo de Adoção (1) : (N) Acompanhamento Pós-Adoção:** um processo de adoção efetivado pode possuir vários registros cronológicos de acompanhamento pós-adoção.
6. **Doador (1) : (N) Doação:** um mesmo doador pode realizar várias doações (financeiras ou materiais) vinculadas ao seu cadastro único.
7. **Voluntário (N) : (N) Atividade (via `VOLUNTARIO_ATIVIDADE`):** um voluntário pode participar de várias atividades, e uma atividade pode contar com vários voluntários (sem vínculos duplicados).
8. **Usuário (1) : (1) Tutor/Adotante:** cada usuário do tipo `TUTOR/ADOTANTE` está associado a um único perfil em `TUTOR_ADOTANTE`.
9. **Administrador:** possui acesso administrativo completo aos módulos do sistema, identificado diretamente pelo atributo `tipo_usuario = ADMINISTRADOR` em `USUARIO`.

## 4. Relacionamentos associativos
Existem dois relacionamentos muitos-para-muitos (N:N) materializados por tabelas associativas no domínio:

1. **Animal ↔ Lar Temporário (`ANIMAL_LAR_TEMPORARIO`):** um animal pode passar por diferentes lares temporários em períodos distintos, e um lar temporário pode acolher diferentes animais ao longo do tempo.
2. **Voluntário ↔ Atividade (`VOLUNTARIO_ATIVIDADE`):** um voluntário pode participar de várias atividades da ONG, e uma atividade pode contar com a participação de vários voluntários. Possui chave primária composta por `(voluntario_id, atividade_id)`.