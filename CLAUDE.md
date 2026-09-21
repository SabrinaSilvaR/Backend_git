# CLAUDE.md

The full, tool-agnostic instructions for this repository live in **[AGENTS.md](./AGENTS.md)**.

@AGENTS.md

Reusable capabilities live in [`.ai/`](./.ai/README.md) — read the relevant file when it applies:

- `.ai/skills/` — OpenSpec spec-driven workflow (optional `spec-intake` on-ramp → `spec-propose` → `spec-design` → `spec-tasks` → `spec-implement` → `spec-archive`, with `spec-conventions` as the format reference), the operating manual (`ways-of-working` — read first) and best-practice skills (`django-orm`, `drf-serializers`, `drf-views`, `django-services`, `django-testing`, `python-typing`, `drf-auth-permissions`).
- `.ai/prompts/` — task playbooks (`create-model`, `create-serializer`, `create-viewset`, `create-service`, `create-test`, `create-migration`, reviews, doc generators).
- `.ai/agents/` — agent roles (`drf-developer`, `django-architect`, `debug`, `mentor`).

To run the spec-driven loop, follow `.ai/skills/spec-<step>.md` (the change folder lives under
`specs/changes/`; living specs under `specs/specs/`). Do not duplicate guidance here — update
`AGENTS.md` or the `.ai/` files instead.