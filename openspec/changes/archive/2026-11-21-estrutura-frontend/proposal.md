## Why

O frontend do Porto Seguro Pet está concentrado inicialmente em um único arquivo, o que pode dificultar a manutenção e a evolução do sistema conforme novas telas e funcionalidades forem implementadas. Esta mudança organiza a estrutura do frontend Reflex para permitir o crescimento do projeto de forma simples, clara e sustentável.

## What Changes

- Organizar o código do frontend em uma estrutura adequada para múltiplas telas e componentes.
- Separar responsabilidades entre páginas, componentes visuais e lógica de estado quando necessário.
- Manter a tela de login existente funcionando após a reorganização.
- Preparar a estrutura para a criação das futuras áreas do TUTOR/ADOTANTE e do ADMINISTRADOR.
- Não alterar as regras de negócio ou o comportamento funcional do sistema nesta mudança.

## Capabilities

### New Capabilities

Nenhuma. Esta mudança é exclusivamente estrutural e não introduz comportamento novo para o usuário.

### Modified Capabilities

Nenhuma.

## Impact

- Frontend em Reflex: reorganização dos arquivos e diretórios do projeto.
- Código da tela de login: poderá ser separado em arquivos próprios sem alteração do comportamento já implementado.
- Não há alteração prevista no backend Xano.
- Não há alteração prevista no banco de dados.
- Não há novas dependências previstas.
