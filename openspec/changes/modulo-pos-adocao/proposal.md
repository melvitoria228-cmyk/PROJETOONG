# Proposta: Módulo de Pós-Adoção (Linha do Tempo de Acompanhamento)

## 1. Motivação e Contexto

Após a efetivação da adoção, a ONG precisa acompanhar a adaptação do animal ao novo ambiente, verificar suas condições e oferecer orientações ao tutor quando necessário.

O módulo de Pós-Adoção permitirá organizar esses registros em uma linha do tempo, facilitando a consulta ao histórico de acompanhamento de cada animal adotado.

A interface utilizará o formato de **Linha do Tempo (Timeline)**, com os registros apresentados em ordem cronológica decrescente, do mais recente para o mais antigo.

## 2. Escopo das Mudanças

- Criação do estado `pos_adocao_state.py` no diretório `state`.
- Criação da interface gráfica `pos_adocao.py` no diretório `modulos_administracao`.
- Registro da rota `/pos-adocao` em `ProjetoONG.py`.
- Exibição dos processos de adoção com status `Adoção efetivada`.
- Exibição das informações dos animais e respectivos tutores, utilizando os relacionamentos já existentes.
- Consulta dos registros de acompanhamento vinculados ao processo de adoção selecionado.
- Inclusão de novos registros na tabela `ACOMPANHAMENTO_POS_ADOCAO`, utilizando os campos existentes.

## 3. Critérios de Aceite

- Interface alinhada à identidade visual da versão V5, respeitando a paleta de cores definida.
- Layout de duas colunas: lista de animais adotados (~30%) e linha do tempo de acompanhamento (~70%).
- Exibição apenas de animais com adoção efetivada.
- Exibição dos registros de acompanhamento em ordem cronológica decrescente.
- Possibilidade de adicionar novos registros vinculados ao processo de adoção correspondente.
- Utilização da estrutura atual do banco de dados, sem criação de novos campos ou alterações nas tabelas existentes.
