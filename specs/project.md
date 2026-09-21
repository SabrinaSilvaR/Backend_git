# Project: Django & DRF Backend (INACAP)

> OpenSpec project context. This is the stable, high-level description of **this** codebase
> that every spec-driven change reads first. Keep it short and current; deep rules live in
> [`AGENTS.md`](../AGENTS.md) and [`.github/instructions/`](../.github/instructions/).

## Stack

- **Language:** Python 3.13+ (Virtualenv `vgit`)
- **Web Framework:** Django 6.1+
- **API Toolkit:** Django REST Framework (DRF) 3.18+
- **Architecture:** Clean Django (Apps: `apiGit`, Configuration: `projectGit`)
- **Database:** SQLite 3 (local development), PostgreSQL ready

## Conventions

- Code, models, serializers, views, and documentation in **English**.
- Business-domain terminology from education/INACAP preserved where explicitly requested.
- Thin views, serializers for validation/representation, domain mutations in `services.py`, queries in `selectors.py`.

## Quality gates

```bash
.\vgit\Scripts\python.exe manage.py check
```

## How specs work here (OpenSpec)

- `specs/specs/` — **living truth**: one folder per capability, the behavior that **is** built.
- `specs/changes/` — **proposals**: each change carries spec **deltas** (`## ADDED|MODIFIED|REMOVED Requirements`). When shipped, `spec-archive` applies the deltas to `specs/specs/` and moves the change to `specs/changes/archive/`.

See the lifecycle in [`.ai/README.md`](../.ai/README.md) and the format in
[`.ai/skills/spec-conventions.md`](../.ai/skills/spec-conventions.md).
