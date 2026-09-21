# AGENTS.md

> Single source of truth for **all** AI coding assistants working in this repository
> (GitHub Copilot, Claude, Gemini, Codex, Cursor, Antigravity, and any agent reading `AGENTS.md`).

This is a modern, production-ready **Python + Django + Django REST Framework (DRF)** backend repository.
It emphasizes type safety, clean architecture (thin views, serializers for validation, services for business logic),
robust API design, and security.

## Educational & Active Learning Mode (CRITICAL)

This repository is actively used by **students learning Django and DRF**. Therefore, all AI assistants MUST follow an **Active Learning & Guided Practice** approach:
- **Do NOT generate complete, turnkey solutions immediately.**
- **Explain the concept:** Break down what Django/DRF component is needed and why.
- **Provide a minimal analogous scaffold or partial snippet:** Show how the pattern works on a sample entity.
- **Hand over the keyboard to the student:** Challenge the student to write the code for their specific model, serializer, or view.
- **Review directly from the repository, never from pasted code:** Do not ask the student to copy/paste their code into the chat. Once they say they wrote it (or name the file), open and read the actual file(s) in the working directory yourself (e.g. `apiGit/models.py`) and review that. Point out what works, edge cases, and PEP 8 lints, referencing exact file paths and line numbers.
- If the student explicitly asks *"muéstrame la solución completa"* or is completely stuck after attempts, provide the solution accompanied by an explanation of each part.

## How to use this document

- This file is the canonical, tool-agnostic instruction set. `CLAUDE.md` and `GEMINI.md`
  are thin pointers to it — **do not** duplicate guidance into those pointers.
- Keep this file as the high-level contract (stack, rules, conventions). Long-form
  detail lives in the deep references in `.github/instructions/`; link to them instead of repeating.
- **Operating manual:** read [`.ai/skills/ways-of-working.md`](.ai/skills/ways-of-working.md) first — the autonomy policy, the Definition of Done, and how to talk to a (possibly non-technical) user.
- User instructions always take precedence — see Priority order below.

## Priority order

When guidance conflicts, resolve in this order:

1. **User instructions** — a direct request in chat.
2. **This file (`AGENTS.md`)** — the canonical, tool-agnostic contract.
3. **Deep references** in [`.github/instructions/`](.github/instructions/) and the canonical
   scaffolds in [`.vscode/__templates__/`](.vscode/__templates__/).
4. **Existing patterns** in the codebase (`apiGit/`, `projectGit/`, and `docs/` where present).

## Tech stack

| Area               | Choice                                                                  |
| ------------------ | ----------------------------------------------------------------------- |
| Language           | Python 3.12+ (tested on Python 3.13+) with PEP 484 type annotations      |
| Web Framework      | Django 6.x (or 5.x LTS)                                                 |
| API Framework      | Django REST Framework (DRF) 3.15+                                       |
| Architecture       | Clean Django / Service-Selector pattern (models, serializers, services) |
| Database           | SQLite (local dev), PostgreSQL (production-ready)                       |
| Authentication     | DRF Token / Session / JWT Authentication + Django Auth                  |
| Validation         | DRF Serializers (declarative field & object-level validation)           |
| Environment/Config | `os.environ` / `python-decouple` / Django settings                      |
| Tooling            | virtualenv (`vgit`), pip, ruff / flake8 / black                         |
| Runtime            | Python 3.13 in `vgit/Scripts/python.exe`                                |

## Commands

Always use the virtualenv executable when running commands:

```bash
# Development server
.\vgit\Scripts\python.exe manage.py runserver

# Database migrations
.\vgit\Scripts\python.exe manage.py makemigrations
.\vgit\Scripts\python.exe manage.py migrate

# Interactive shell
.\vgit\Scripts\python.exe manage.py shell

# Create superuser
.\vgit\Scripts\python.exe manage.py createsuperuser

# Linting & code formatting (if installed)
ruff check .
black .
```

Verify migrations before finalizing non-trivial changes.

## Project structure

```
apiGit/                 # Django App (features, domain models, serializers, views, services)
  models.py             # Domain models (ORM)
  serializers.py        # DRF Serializers (validation & transformation)
  views.py              # API views / ViewSets
  urls.py               # App-specific URL route configuration
  services.py           # Business logic & mutations (write operations)
  selectors.py          # Data fetching & query building (read operations)
  admin.py              # Django admin registrations
projectGit/             # Django Project Configuration
  settings.py           # Project settings, installed apps, middleware, databases
  urls.py               # Root URL configuration (includes apiGit.urls)
  wsgi.py / asgi.py     # Deployment entrypoints
specs/                  # OpenSpec living specifications and changes
.ai/                    # AI skills, prompts, agents, and templates
.github/instructions/   # Deep references (architecture, standards, patterns)
.vscode/__templates__/  # Canonical code scaffolds for Django/DRF components
```

When creating a new file or component, start from the matching scaffold under
[`.vscode/__templates__/`](.vscode/__templates__/) — it is the source of truth for
naming, signatures, and patterns.

## Core principles

- **Type hints first** — use Python type annotations (`typing`) across functions, methods, and services.
- **Thin views, fat services** — keep views and ViewSets thin (handling HTTP, request parsing, and response formatting); delegate business logic and complex writes to `services.py`, and complex reads to `selectors.py`.
- **Validation in serializers** — leverage DRF `Serializer` and `ModelSerializer` for request validation (`validate_<field>`, `validate`), keeping data contracts strict and secure.
- **ORM query optimization** — always prevent N+1 queries using `select_related()` for ForeignKey/OneToOne and `prefetch_related()` for ManyToMany/reverse relationships.
- **Security by default** — never commit secrets, passwords, or production SECRET_KEYs; restrict permissions on sensitive endpoints using DRF `permission_classes = [IsAuthenticated]`.
- **YAGNI** — minimal, atomic changes; no speculative over-engineering.

## Critical rules

These are non-negotiable. Violations must be fixed before code is considered done.

### Configuration & secrets

- **NEVER** commit plain-text credentials, database passwords, API keys, or secret tokens.
- Keep environment-specific settings managed via environment variables or `.env` files.
- Never set `DEBUG = True` or `ALLOWED_HOSTS = ['*']` in production configurations.

### Language policy

- Code, documentation, variable names, and commit messages are in **English** — identifiers, docstrings, comments, errors.
- **Domain exception:** preserve business-domain terms in their original language when explicitly defined as domain entities (e.g. `InacapEstudiante`, `Asignatura`). Technical code around them stays in English.

### Architecture & layering

- **Models (`models.py`):** Define fields, constraints, string representations (`__str__`), and Meta options. Keep models focused on data schema.
- **Serializers (`serializers.py`):** Handle deserialization, validation, and serialization. Always specify explicit `fields` instead of `'__all__'`.
- **Services (`services.py`):** Write operations, domain transactions (`@transaction.atomic`), business rules, sending notifications.
- **Selectors (`selectors.py`):** Read-only queries, complex filters, aggregations.
- **Views (`views.py`):** Receive request, pass data to serializer/service/selector, return `Response`.

### Accessibility & REST conventions

- Follow RESTful principles: use standard HTTP methods (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`) and appropriate HTTP status codes (`200 OK`, `201 Created`, `204 No Content`, `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`).

## Code style (essentials)

- Follow **PEP 8** style guide: 4 spaces for indentation, snake_case for functions and variables, PascalCase for classes, UPPER_SNAKE_CASE for constants.
- Group imports logically:
  1. Standard library imports (e.g. `datetime`, `uuid`)
  2. Third-party imports (e.g. `django.*`, `rest_framework.*`)
  3. Local application imports (e.g. `from .models import ...`)
- Maximum line length ~88–100 characters.
- Add descriptive docstrings to classes and public service functions.

Full ruleset and anti-patterns: [`.github/instructions/coding-standards.instructions.md`](.github/instructions/coding-standards.instructions.md).

## Commit conventions

Use **Conventional Commits with Gitmoji**:

```
<type>(<optional scope>) <gitmoji>: <description>
```

Examples:

```
feat(api) ✨: add student registration endpoint
fix(serializers) 🐛: resolve date validation error
refactor(services) ♻️: extract grading calculation to service
chore(deps) 🔧: update djangorestframework
```

Common types: `feat` ✨, `fix` 🐛, `docs` 📚, `style` 🎨, `refactor` ♻️, `perf` ⚡, `chore` 🔧.

## Spec-driven development (SDD)

Build features through a spec-first loop following the **OpenSpec** convention
([openspec.dev](https://openspec.dev)): living specs are the current truth, and each request
is a **change** carrying spec **deltas** that get applied on ship.
The procedures live in [`.ai/skills/`](.ai/skills/):

```
/spec-intake    rough idea → an idea brief (optional on-ramp: shape a detailed input)
/spec-propose   idea    → specs/changes/<id>/proposal.md + specs/<cap>/spec.md deltas (what + why)
/spec-design    change  → specs/changes/<id>/design.md   (technical design; skip if trivial)
/spec-tasks     change  → specs/changes/<id>/tasks.md    (atomic, test-first tasks)
/spec-implement change  → code + tests (makemigrations → run tests → refactor)
/spec-archive   change  → verify + apply deltas to specs/specs/ + move to specs/changes/archive/
```

Folder model (root `specs/`): `specs/specs/` = **living truth** (one folder per capability);
`specs/changes/<id>/` = **proposals** with `## ADDED|MODIFIED|REMOVED Requirements` deltas;
`specs/changes/archive/YYYY-MM-DD-<id>/` = shipped changes (the durable decision log).

## Deep references

| Document                                                                      | Scope                                                                                                             |
| ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| [Operating manual](.ai/skills/ways-of-working.md)                             | Autonomy, default technical decisions, Definition of Done, user communication                                     |
| [Architecture guide](.github/instructions/architecture-guide.instructions.md) | Django/DRF topology, services/selectors wiring, URL routing, model relationships                                   |
| [Coding standards](.github/instructions/coding-standards.instructions.md)     | PEP 8, naming conventions, type hints, import ordering, REST anti-patterns                                        |
| [Patterns](.github/instructions/patterns.instructions.md)                     | Copy-paste recipes: models, serializers, viewsets, services, permissions, tests                                   |
| [Code exemplars](exemplars.md)                                                | Pointers to high-quality real examples in this repo                                                               |
| [README](README.md)                                                           | Project overview and quickstart                                                                                   |
| [`.vscode/__templates__/`](.vscode/__templates__/)                            | Canonical code scaffolds for every Django/DRF pattern                                                             |
