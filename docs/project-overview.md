## Finalidade deste documento
Apresentar uma visão geral consolidada do **Sistema Porto Seguro Pet**, servindo como referência técnica e funcional para sua compreensão, manutenção e evolução.

## 1. Visão geral do projeto
O **Porto Seguro Pet** é um sistema web centralizado de gerenciamento desenvolvido para uma ONG de proteção animal, que organiza informações e processos relacionados aos animais resgatados — desde os cuidados iniciais, atendimento veterinário e acolhimento em lares temporários até a adoção responsável e o acompanhamento pós-adoção.

Além do ciclo completo dos animais, o sistema gerencia informações de tutores/adotantes, voluntários, atividades da ONG, doadores e doações financeiras e materiais.

## 2. Problema
A desorganização e dispersão das informações e dos processos internos da ONG dificultavam o acompanhamento atualizado do histórico de cada animal, a triagem de solicitações de adoção e o controle integrado das atividades administrativas e operacionais.

## 3. Objetivos
- Organizar e centralizar as informações operacionais e cadastrais da ONG em um banco de dados único.
- Gerenciar o ciclo completo de atendimento dos animais, desde o resgate até a adoção e o acompanhamento pós-adoção.
- Apoiar a gestão de lares temporários, atendimentos veterinários, tutores/adotantes, voluntários, atividades e doações.
- Disponibilizar um portal dedicado para que tutores/adotantes acompanhem seus processos de adoção, registros de pós-adoção e orientações de guarda responsável.

## 4. Usuários
- **Tutor/Adotante (`TUTOR/ADOTANTE`):** realiza login, visualiza animais disponíveis, envia solicitações de adoção, acompanha o status de seus processos e registros de pós-adoção, consulta/atualiza seus dados cadastrais e acessa orientações de cuidados.
- **Administrador (`ADMINISTRADOR`):** possui acesso completo à Área Administrativa e a todos os módulos operacionais da ONG.

## 5. Escopo
O sistema contempla o gerenciamento integrado dos 9 processos centrais da ONG:
1. Avaliação e solicitação de resgate (triagem prévia ao cadastro).
2. Resgate e cuidados iniciais.
3. Lar temporário e histórico de acolhimento.
4. Processo de adoção (solicitação, análise, aprovação e efetivação).
5. Acompanhamento pós-adoção.
6. Atendimento veterinário (agendamento, prontuário clínico e histórico).
7. Gestão de voluntários e atividades.
8. Gestão de doações (financeiras e materiais) e cadastro único de doadores.
9. Gestão administrativa centralizada, autenticação e recuperação de senha.

## 6. Principais funcionalidades
1. Autenticação por perfil (`ADMINISTRADOR` e `TUTOR/ADOTANTE`) e recuperação/redefinição de senha.
2. Gerenciamento completo de animais resgatados (CRUD, filtros, status, alergias e restrições clínicas).
3. Gerenciamento de lares temporários e histórico de permanência (`ANIMAL_LAR_TEMPORARIO`).
4. Agendamento e registro clínico de atendimentos veterinários (`ATENDIMENTO_VETERINARIO`).
5. Triagem, aprovação/recusa e efetivação de processos de adoção (`PROCESSO_ADOCAO`).
6. Registro cronológico (*timeline*) de acompanhamento pós-adoção (`ACOMPANHAMENTO_POS_ADOCAO`).
7. Gerenciamento de voluntários, atividades e vínculos de participação (`VOLUNTARIO_ATIVIDADE`).
8. Cadastro único de doadores e registro de doações financeiras e materiais (`DOADOR` e `DOACAO`).
9. Portal exclusivo do Tutor/Adotante (`/tutor`) integrado aos processos da ONG.

## 7. Requisitos e restrições
1. O sistema deve manter todas as informações organizadas e centralizadas no banco de dados relacional.
2. O cadastro do animal ocorre somente após o resgate aprovado; solicitações não aprovadas não geram registro permanente.
3. A aprovação de uma solicitação de adoção (`Aprovada`) não conclui o processo; a adoção só é efetivada (`Adoção efetivada`) após a entrega ou retirada do animal, momento em que o status do animal passa automaticamente para `Adotado`.
4. O acompanhamento pós-adoção permite registros cronológicos flexíveis conforme a necessidade de cada caso.
5. As doações materiais registram a descrição dos itens e a data de recebimento para fins documentais e de histórico, não realizando controle de movimentação de estoque.
6. Cadastros de e-mail (`USUARIO`), CPF (`TUTOR_ADOTANTE` e `DOADOR`) e vínculos voluntário-atividade (`VOLUNTARIO_ATIVIDADE`) devem impedir duplicidades.

## 8. Tecnologias e arquitetura
- **Frontend:** Python 3 com **Reflex** (arquitetura modular separando `*_state.py` para estados reativos/handlers e `*.py` para interfaces).
- **Backend & Banco de Dados:** **Xano** (API REST e banco de dados relacional).
- **Integração HTTP & Configuração:** `httpx.AsyncClient` e variáveis de ambiente via `.env`.
- **Versionamento:** Git e GitHub.
- **Especificação:** OpenSpec (`openspec/`).

## 9. Princípios de desenvolvimento
- Manter o sistema simples, claro e funcional.
- Respeitar rigorosamente as regras de negócio e o modelo relacional definidos para o domínio.
- Evitar estruturas ou complexidades desnecessárias ao escopo da ONG.
- Manter a documentação, o código e as especificações sincronizados.

## 10. Segurança e integridade
- Controle de acesso baseado em token **JWT** e segregação de rotas por perfil (`ADMINISTRADOR` vs `TUTOR/ADOTANTE`).
- Validação de unicidade de identificadores críticos (e-mail, CPF e chave composta em tabelas associativas) e sincronização automática de status dependentes.
- Validação de segurança na redefinição de senha (critérios mínimos de força e confirmação idêntica antes do envio).

## 11. Estratégia de desenvolvimento
- Desenvolvimento orientado por especificações (**OpenSpec**), evoluindo cada módulo por meio de propostas, tarefas e especificações validadas antes do arquivamento.
- Implementação incremental por módulos independentes conectados a uma navegação administrativa unificada e ao portal do tutor.
- Validação contínua de sintaxe (`py_compile`), integridade das chamadas assíncronas com o Xano e conformidade das especificações.