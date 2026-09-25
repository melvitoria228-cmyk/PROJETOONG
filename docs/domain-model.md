## 1. Visão do domínio
O domínio do Porto Seguro Pet representa os processos de uma ONG de proteção animal, envolvendo o gerenciamento dos animais desde o resgate até a adoção e o acompanhamento pós-adoção, além da gestão de tutores/adotantes, voluntários, doadores, doações e suprimentos.

## 2. Principais conceitos do domínio
1.Animal: representa os animais atendidos pela ONG.

2.Lar Temporário: representa os locais onde os animais podem permanecer temporariamente.

3.Atendimento Veterinário: representa os atendimentos e cuidados veterinários realizados.

4.Tutor/Adotante: representa a pessoa que utiliza o sistema para participar e acompanhar um processo de adoção.

5.Usuário: representa o acesso ao sistema, podendo estar associado a um tutor/adotante ou possuir acesso administrativo.

6.Processo de Adoção: representa a solicitação, avaliação e acompanhamento do processo de adoção de um animal por um tutor/adotante.

7.Acompanhamento Pós-Adoção: representa o acompanhamento realizado após a adoção.

8.Voluntário: representa as pessoas que atuam nas atividades da ONG.

9.Atividade: representa as atividades realizadas pela ONG com participação de voluntários.

10.Doador: representa quem realiza doações financeiras.

11.Doação: representa as doações financeiras realizadas.

12.Estoque de Suprimentos: representa os materiais e suas quantidades disponíveis. 

13.Movimentação de Estoque: representa as entradas e saídas de suprimentos.

## 3.Relacionamentos do domínio
1.Animal pode possuir vários registros de lar temporário.

2.Animal pode possuir vários atendimentos veterinários.

3.Animal pode possuir vários processos de adoção.

4.Tutor/Adotante pode participar de vários processos de adoção.

5.Processo de Adoção pode possuir vários registros de acompanhamento pós-adoção.

6.Doador pode realizar várias doações financeiras.

7.Estoque de Suprimentos pode possuir várias movimentações de estoque.

8.Voluntário pode participar de várias atividades, e uma atividade pode contar com vários voluntários.

9.Usuário pode estar associado a um Tutor/Adotante.

10.Administrador possui acesso administrativo aos processos do sistema e é identificado pelo tipo de usuário.

## 4. Relacionamentos associativos
Existem dois relacionamentos muitos-para-muitos no domínio:

1.Animal ↔ Lar Temporário: um animal pode passar por diferentes lares temporários, e um lar pode receber diferentes animais. Esse relacionamento é representado por ANIMAL_LAR_TEMPORARIO.

2.Voluntário ↔ Atividade: um voluntário pode participar de várias atividades, e uma atividade pode contar com vários voluntários. Esse relacionamento é representado por VOLUNTARIO_ATIVIDADE.

