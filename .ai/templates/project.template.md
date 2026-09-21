# Project: <Project Name>

> OpenSpec project context. Stable, high-level description of this codebase that every
> spec-driven change reads first.

## Stack

- **Language:** Python 3.13+
- **Framework:** Django 6.x / Django REST Framework 3.15+
- **Database:** SQLite (local dev), PostgreSQL (production)
- **Architecture:** Clean Django (Apps, Models, Serializers, Services, Selectors, Views)
- **Testing:** Django TestCase & `rest_framework.test.APITestCase`

## Quality gates

```bash
.\vgit\Scripts\python.exe manage.py test apiGit
.\vgit\Scripts\python.exe manage.py makemigrations --check --dry-run
```
