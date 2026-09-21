# `.ai/` — Spec-driven AI development layer for Django & DRF

Tool-neutral home for the **OpenSpec spec-driven development (SDD)** workflow and reusable
best-practice skills for Python, Django, and Django REST Framework. This is the single source of truth for skill
procedures, task prompts, and agent roles; each AI tool gets a thin adapter that points here
(same philosophy as [`AGENTS.md`](../AGENTS.md)).

**Start with [`skills/ways-of-working.md`](skills/ways-of-working.md)** — the operating manual
that makes agents autonomous and usable by non-technical people: when to act vs. ask, the
default technical decisions, the single Definition of Done, and how to talk to the user.

## Layout

```
.ai/
  skills/          canonical skill bodies (the real procedures)
    ways-of-working.md       ← operating manual: read first
    spec-intake.md           # optional on-ramp: guided interview to shape ideas into specs
    spec-propose.md          spec-design.md  spec-tasks.md  spec-implement.md  spec-archive.md
    spec-conventions.md      # OpenSpec format & folder-model reference
    django-orm.md            django-services.md  drf-serializers.md  drf-views.md
    drf-auth-permissions.md  django-testing.md   python-typing.md
  prompts/         canonical task-prompt bodies (create-model, create-serializer,
                   create-viewset, create-service, create-test, create-migration,
                   code-quality-improvement, security-review, review-and-refactor,
                   architecture-blueprint-generator, technology-stack-blueprint-generator,
                   update-instructions)
  agents/          canonical agent definitions (drf-developer, django-architect, debug, mentor)
  templates/       artifact templates used by the spec skills
    idea.template.md  project.template.md  proposal.template.md  design.template.md
    tasks.template.md  spec.template.md  delta.template.md
specs/             OpenSpec workspace (root)
  project.md       stable project context (read first)
  specs/           living truth — one folder per capability (<capability>/spec.md)
  changes/         active proposals (<change-id>/proposal.md, design.md, tasks.md, specs/ deltas)
    archive/       shipped changes (YYYY-MM-DD-<change-id>/) — the decision log
```

## The spec-driven loop (OpenSpec)

Living specs are the current truth; each request is a **change** (like a DB migration) that
carries spec **deltas** and gets applied on ship. See `skills/spec-conventions.md` for the
exact format.

```
AGENTS.md (constitution) + specs/project.md (context)
  → /spec-intake    rough idea → an idea brief (optional on-ramp)
  → /spec-propose   idea    → specs/changes/<id>/proposal.md + specs/<cap>/spec.md deltas (what + why)
  → /spec-design    change  → specs/changes/<id>/design.md   (technical design; skip if trivial)
  → /spec-tasks     change  → specs/changes/<id>/tasks.md    (atomic, test-first tasks)
  → /spec-implement change  → code + tests (makemigrations → python manage.py test → refactor)
  → /spec-archive   change  → verify + apply deltas to specs/specs/ + move to specs/changes/archive/
```

Every step respects `AGENTS.md` and the deep docs in `.github/instructions/`. The
`spec-implement` step runs against the local virtualenv toolchain:
`.\vgit\Scripts\python.exe manage.py makemigrations` → `.\vgit\Scripts\python.exe manage.py migrate` → `.\vgit\Scripts\python.exe manage.py test`.

## Best-practice & reference skills

Beyond the SDD loop, `skills/` holds best-practice skills any tool can read on demand:
- `django-orm`: Schema modeling, indexing, queries, avoiding N+1.
- `drf-serializers`: Input validation, transformation, serializer fields.
- `drf-views`: APIView, ViewSets, Routers, filtering, pagination.
- `django-services`: Business logic & mutations isolated from views.
- `django-testing`: APITestCase, APIClient, mocking, test fixtures.
- `python-typing`: Modern Python type hints and typing conventions.
- `drf-auth-permissions`: Authentication schemes and role-based permissions.

## How each tool reaches these files

| Tool           | How it reaches `.ai/`                                                                                                                                                                 |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GitHub Copilot | Native thin pointers under `.github/`: `prompts/*.prompt.md`, `agents/*.agent.md`. Invoked as `/spec-propose`, `/create-serializer`, etc.                                             |
| Claude Code    | `CLAUDE.md` links here — reads `.ai/` directly: point the agent at `.ai/skills/spec-<step>.md`, `.ai/prompts/<task>.md`, or `.ai/agents/<role>.md`.                                   |
| Gemini CLI     | `GEMINI.md` links here — same as Claude.                                                                                                                                              |
| Antigravity / Cursor | Reads `AGENTS.md` directly and accesses `.ai/skills/` and `.ai/prompts/`.                                                                                                       |
