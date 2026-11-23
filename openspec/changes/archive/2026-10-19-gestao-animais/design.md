## Context

O projeto **Porto Seguro Pet** utiliza **Reflex** no frontend e **Xano** no backend. A tabela `ANIMAL` e seus endpoints REST (`GET`, `POST`, `PATCH`, `DELETE`) estão configurados no grupo de API `PortoSeguroPet` no Xano.

A aplicação possui autenticação baseada em token JWT (`LoginState`) e uma estrutura modular na Área Administrativa, com menu lateral fixo (`sidebar_administracao`) e rotas dedicadas por operação. O módulo de Gestão de Animais opera na rota `/animais` com carregamento automático (`on_load`), integrando os dados do Xano à interface administrativa.

Os requisitos funcionais desta mudança estão definidos em `specs/gestao-animais/spec.md`.

## Goals / Non-Goals

**Goals:**

- Integrar a tela de Gestão de Animais (`/animais`) aos endpoints REST da tabela `ANIMAL` no Xano utilizando requisições assíncronas autenticadas (`httpx`).
- Modularizar a interface e o gerenciamento de estado em arquivos dedicados (`gestao_animais.py` e `animais_state.py`), reutilizando o menu lateral unificado (`sidebar_administracao`) de `ProjetoONG.py`.
- Seguir a identidade visual administrativa definida para o projeto (paleta Terracota, Verde Oliva e Areia).
- Suportar indicadores resumidos (KPIs), busca textual, filtros combinados, paginação e exibição/ampliação de fotografias via URL (`foto_url`).
- Tratar resultados e falhas das operações com feedback claro via *toast* sem apresentar mensagens de sucesso indevidas.
- Respeitar os campos, os status e a integridade referencial dos relacionamentos no banco de dados.

**Non-Goals:**

- Criar uma nova tabela `ANIMAL` ou duplicar os endpoints existentes no Xano.
- Implementar upload de arquivos binários pesados de imagem (mantendo o armazenamento leve por URL em `foto_url`).
- Alterar o mecanismo de autenticação JWT ou introduzir subperfis administrativos nesta entrega.
- Adicionar dependências externas desnecessárias além dos componentes nativos do Reflex e `httpx`.

## Decisions

### 1. Modularizar a interface e o estado da Gestão de Animais

A implementação foi organizada de forma modular para facilitar a manutenção e evitar sobrecarga no arquivo principal:

- **`animais_state.py` (`AnimaisState`):** concentra as variáveis de estado da listagem, filtros, paginação, formulários de criação/edição, modal de foto ampliada e os manipuladores assíncronos (`httpx`) de comunicação com o Xano.
- **`gestao_animais.py` (`pagina_gestao_animais`):** define os cartões de KPIs, barra de busca e filtros, tabela responsiva com miniaturas clicáveis e modais de visualização, cadastro, edição e exclusão.
- **`ProjetoONG.py`:** registra a rota dedicada `/animais` com disparo automático de carregamento no `on_load` e integra o menu lateral unificado `sidebar_administracao()`.

**Alternativa considerada:** manter toda a implementação diretamente dentro de `ProjetoONG.py`. Embora viável inicialmente, a separação em módulos dedicados tornou o código mais limpo, legível e alinhado aos demais módulos administrativos.

### 2. Utilizar o Xano como fonte persistente de dados com autenticação JWT

As operações de consulta (`GET`), cadastro (`POST`), edição (`PATCH`) e exclusão (`DELETE`) comunicam-se diretamente com os endpoints da tabela `ANIMAL` no grupo de API `PortoSeguroPet` no Xano.

- A URL do endpoint é carregada via variável de ambiente (`XANO_ANIMAL_URL`) definida no arquivo `.env` (protegido pelo `.gitignore`).
- As requisições enviam o cabeçalho `Authorization: Bearer <token>` recuperado da sessão autenticada (`LoginState.token`).
- Todas as chamadas são executadas de forma assíncrona com `httpx.AsyncClient`, garantindo fluidez na interface e tratamento explícito de códigos HTTP e exceções de rede.

**Alternativa considerada:** manter os registros apenas em memória local no frontend. Descartada pela necessidade de persistência real e compartilhamento de dados entre os módulos de adoção, atendimento veterinário e lares temporários.

### 3. Preservar o modelo de dados existente e suportar `foto_url`

A interface mapeia fielmente os campos de negócio definidos na entidade `ANIMAL` no Xano:

- `nome`: texto obrigatório.
- `especie`: texto (`Cão`, `Gato`, `Outros`).
- `raca`: texto.
- `idade_estimada`: número inteiro (em meses).
- `sexo`: texto (`Macho`, `Fêmea`, `Não identificado`).
- `porte`: texto (`Mini`, `Pequeno`, `Médio`, `Grande`).
- `condicao_saude`: texto.
- `status_atual`: texto (`Disponível`, `Em Lar Temporário`, `Em Processo de Adoção`, `Adotado`, `Falecido`).
- `data_resgate`: data.
- `foto_url`: texto opcional contendo o link direto da fotografia do animal, exibida como avatar circular na listagem e expansível em modal.

Os campos de identificação e auditoria (`id`, `created_at`) são gerenciados exclusivamente pelo Xano e exibidos apenas para consulta.

**Alternativa considerada:** alterar os valores padronizados de status ou criar tabelas auxiliares para imagens. Evitado para preservar total compatibilidade com os registros existentes e demais endpoints do backend.

### 4. Separar os estados de consulta, filtragem e edição

O `AnimaisState` mantém separadas:
- a lista principal sincronizada com o backend;
- as propriedades computadas/filtradas para busca textual, filtros por espécie/porte/status e paginação;
- os campos temporários dos formulários de cadastro e edição.

Após uma operação `POST` ou `PATCH` confirmada pelo Xano, a listagem é recarregada com os dados atualizados do servidor. Em caso de erro, o estado anterior é preservado e uma notificação *toast* de erro é exibida ao administrador.

**Alternativa considerada:** aplicar atualização otimista na tabela antes da resposta do servidor. Descartada para evitar inconsistências visuais caso o backend rejeite a operação.

### 5. Tratar a exclusão com confirmação e proteção de integridade

Antes de enviar qualquer requisição `DELETE` ao Xano, o sistema exige confirmação explícita do administrador por meio de um modal dedicado.

- Se o usuário cancelar, nenhuma requisição é disparada.
- Caso o Xano bloqueie a exclusão devido a vínculos ativos com outras entidades (`PROCESSO_ADOCAO`, `ATENDIMENTO_VETERINARIO` ou `ANIMAL_LAR_TEMPORARIO`) ou ocorra falha de comunicação, o registro permanece na listagem e uma mensagem informativa explica o motivo da recusa.

**Alternativa considerada:** exclusão direta em um clique na tabela. Descartada pelo alto risco de perda acidental de registros vinculados.

### 6. Seguir a identidade visual unificada da Área Administrativa

A tela adota a paleta institucional padronizada em toda a Área Administrativa do Porto Seguro Pet:

- **Menu Lateral (`sidebar_administracao`):** fundo Areia (`#EFE6DA`) com borda `#E2D7C7` e item ativo destacado em branco (`#FFFFFF`).
- **Área de Conteúdo:** fundo Bege Claro (`#F8F3EC`) para conforto visual.
- **Terracota Institucional:** `#A96348` / `#A65F43` (hover `#8F503B` / `#C77D5B`) e suave `#F5E7DF` para botões principais, ícones e destaques.
- **Verde Oliva:** `#737747` (hover `#A3A66B`) e suave `#E5E6CF` para indicadores positivos e status disponíveis.
- **Caramelo / Areia:** `#8C6239` / `#D6B99A` para bordas, detalhes e avatares neutros quando o pet não possui `foto_url`.
- **Tipografia:** Café Escuro (`#2D1F18`) para títulos; Marrom Médio (`#52433D`) para textos; Cinza Quente (`#78675E`) para rótulos e metadados.

Os badges de status combinam cores suaves de fundo com texto legível, garantindo acessibilidade e leitura rápida na tabela.

## Risks / Trade-offs

- **Falha de comunicação ou timeout com o Xano** → tratada com blocos `try/except` assíncronos no `AnimaisState`, exibindo mensagem clara via *toast* sem alterar o estado validado.
- **Links externos inválidos em `foto_url`** → fallback automático para avatar neutro estilizado com ícone de pata (`paw-print`), evitando ícones de imagem quebrada na tabela.
- **Exclusão bloqueada por relacionamentos ativos** → interceptação do código de erro HTTP retornado pelo Xano e exibição de orientação clara ao usuário.
- **Exposição de configurações sensíveis** → URLs de API isoladas em `.env` e uso restrito do token JWT em memória de sessão.

## Migration Plan

1. Configurar a variável `XANO_ANIMAL_URL` no `.env` e validar os endpoints CRUD da tabela `ANIMAL` no Xano.
2. Implementar `animais_state.py` e `gestao_animais.py` seguindo a paleta institucional e o layout com `sidebar_administracao`.
3. Registrar a rota `/animais` em `ProjetoONG.py` com `on_load` vinculado ao carregamento inicial do `AnimaisState`.
4. Validar em ambiente local os fluxos de listagem, KPIs, filtros, paginação, visualização com ampliação de foto, cadastro, edição, exclusão e tratamento de erros.