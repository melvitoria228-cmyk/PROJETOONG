<!-- reflex managed begin (do not edit inside this block; add custom content outside the markers) -->
# Agents

This project uses the **Reflex agent skills** — up-to-date knowledge for building full-stack Python web apps with [Reflex](https://reflex.dev). Install them first, then use them as described below.

## Installing the Skills

Before working on this project, make sure the Reflex skills are available to you.

### Claude Code

If the skills are not already available, install them yourself by running these shell commands:

```bash
claude plugin marketplace add reflex-dev/agent-skills
claude plugin install reflex@reflex-agent-skills
```

Newly installed plugins load on the next session. After installing, tell the user to restart the session so the skills auto-load; until then, read the skill files directly from `~/.claude/plugins/` when you need them.

### Other agents (Cursor, OpenCode, Codex, Pi)

```
npx skills add reflex-dev/agent-skills
```

Or clone https://github.com/reflex-dev/agent-skills and copy the `skills/` folders into your agent's skill directory (see the repo README for paths).

### Verifying

Before writing or editing any Reflex code, confirm these three skills are available: `reflex-docs`, `setup-python-env`, and `reflex-process-management`. If they are not, STOP and run the install step above — do not proceed without them.

## Using the Skills

### Reflex documentation

For anything about Reflex APIs — components, state management, events, styling, database, routing, authentication — use the **reflex-docs** skill rather than relying on memory. It carries current, version-accurate docs.

### Initializing a new Reflex project

When starting a new Reflex project or setting up a development environment, you **must** follow the **setup-python-env** skill before doing anything else.

Do not skip any steps. Do not assume a virtual environment or Reflex is already available — always verify first by following the skill's instructions in order.

After the environment is ready and Reflex is installed, run:

```bash
reflex init
```

Then proceed with the user's request.

### Managing a Reflex process

When you need to compile, run, reload, or debug a Reflex application, follow the **reflex-process-management** skill for the correct sequence and error investigation steps.
<!-- reflex managed end -->





# Instruções para a IA

## 1. Consulta à documentação

Antes de realizar mudanças relevantes no projeto, consultar:

* `docs/project-overview.md`
* `docs/domain-model.md`
* `openspec/config.yaml`

As alterações devem respeitar o escopo, os conceitos do domínio, as regras do projeto e a arquitetura definida.

## 2. Arquitetura

Respeitar as tecnologias e responsabilidades definidas para o projeto:

* Frontend: Reflex
* Backend: Xano

Não substituir ou alterar a arquitetura sem uma mudança previamente definida e revisada.

## 3. Desenvolvimento

* Manter o sistema simples e enxuto.
* Evitar funcionalidades, estruturas ou dependências desnecessárias.
* Reutilizar código existente quando possível.
* Evitar duplicação de código.
* Não modificar funcionalidades que não estejam relacionadas à mudança solicitada.

## 4. OpenSpec

Mudanças relevantes devem seguir o fluxo definido pelo OpenSpec.

Antes da implementação, a mudança deve ser especificada e revisada conforme o processo definido no projeto.

Não implementar mudanças relevantes diretamente sem a especificação correspondente.

## 5. Verificação

Após implementar uma mudança:

* Verificar se a implementação corresponde à especificação.
* Verificar se as regras do projeto foram preservadas.
* Verificar se não foram introduzidas alterações desnecessárias ou fora do escopo.

## 6. Código
Manter o código organizado e consistente com a estrutura existente.
Preferir alterações pequenas e relacionadas à tarefa.
Não remover ou alterar código existente sem necessidade.
Manter a implementação coerente com a documentação do projeto.