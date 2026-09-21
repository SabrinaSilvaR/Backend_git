---
applyTo: '**/*.py'
description: 'Folder topology, app structure, layering (models, serializers, views, services, selectors), and URL routing conventions'
---

# Architecture Guide

Deep reference for **where code lives and how it is wired** in this Django + DRF backend.
For high-level rules see [AGENTS.md](../../AGENTS.md); for coding standards see [coding-standards](coding-standards.instructions.md);
for copy-paste recipes see [patterns](patterns.instructions.md).

## Top-level layout

```
apiGit/                 # Feature Django App
  models.py             # ORM models (table schemas, constraints, field types)
  serializers.py        # DRF serializers (input validation, transformation, output schemas)
  views.py              # API views & ViewSets (HTTP routing, status codes, auth checks)
  urls.py               # Route endpoints registered via DefaultRouter or urlpatterns
  services.py           # Business domain mutations & transaction blocks (writes)
  selectors.py          # Query optimization, filtering, and data retrieval (reads)
  admin.py              # Django administration configuration
  tests/                # Automated tests (APITestCase)
    __init__.py
    test_models.py
    test_serializers.py
    test_views.py
projectGit/             # Root Django Project
  settings.py           # Configuration: INSTALLED_APPS, DATABASES, REST_FRAMEWORK
  urls.py               # Root url routing, including apiGit.urls
  wsgi.py / asgi.py     # Deployment entrypoints
manage.py               # Django management CLI entrypoint
specs/                  # Living specs and change proposals (OpenSpec)
.ai/                    # AI workflow, skills, prompts, agents
.vscode/__templates__/  # Code generation templates
```

## Layering & Responsibility Separation

```
Client (HTTP Request)
      │
      ▼
urls.py (Routing)
      │
      ▼
views.py (ViewSet / APIView)
      │
      ├─► Authentication & Permissions (IsAuthenticated)
      ├─► serializers.py (Input validation via is_valid())
      │
      ├─► selectors.py (Read operations -> select_related/prefetch_related)
      │         │
      │         ▼
      │      models.py (Django ORM Queries)
      │
      └─► services.py (Write operations -> @transaction.atomic)
                │
                ▼
             models.py (Django ORM Persistence & Signals)
```

1. **`models.py`**:
   - Represents tables in database.
   - Contains fields, custom managers, `Meta` definitions, and `__str__`.
   - Never contains complex business logic or HTTP-specific logic.

2. **`serializers.py`**:
   - Parses incoming JSON into Python dictionaries and validates schema.
   - Serializes model instances or python dictionaries into outgoing JSON.
   - Contains `validate_<field>` and `validate` methods.

3. **`services.py`**:
   - Contains functions that mutate database state (create, update, delete).
   - Encapsulates domain logic, sending emails, generating reports, payment processing.
   - Uses `@transaction.atomic` when multiple tables or steps are involved.

4. **`selectors.py`**:
   - Encapsulates database read logic.
   - Pre-optimizes querysets (`select_related`, `prefetch_related`, `only`, `defer`).
   - Keeps views completely decoupled from complex ORM queries.

5. **`views.py`**:
   - Thin glue between HTTP and the service/selector layers.
   - Validates user permissions, invokes serializers and services, returns `Response`.
