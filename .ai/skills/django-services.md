# Skill: Django Services & Selectors Architecture

Guidelines for separating domain business logic from HTTP views and ORM models.

## Why Services & Selectors?

- Keeps models focused purely on data definition and simple properties.
- Keeps views thin, testable, and focused only on HTTP serialization.
- Makes business logic easy to test in isolation without invoking full HTTP request cycles.
- Promotes reusable domain logic across API views, management commands, and background tasks.

## Services (`services.py`) — Mutations & Business Logic

- Services perform **write** actions: creating, updating, deleting records, orchestrating side effects (sending emails, logging, calling third-party APIs).
- Always type-hint arguments and return types.
- Wrap multi-table operations in `@transaction.atomic`.

```python
from django.db import transaction
from .models import Student

@transaction.atomic
def register_student(*, first_name: str, last_name: str, email: str) -> Student:
    """Registers a new student and handles associated setup."""
    student = Student.objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email.lower().strip(),
        is_active=True,
    )
    # Side effects (e.g. send_welcome_email(student))
    return student
```

## Selectors (`selectors.py`) — Queries & Reads

- Selectors perform **read** queries: fetching, filtering, aggregating.
- Never modify database state inside a selector.
- Use `select_related()` and `prefetch_related()` to optimize query execution.

```python
from django.db.models import QuerySet
from .models import Student

def list_active_students(*, search_query: str | None = None) -> QuerySet[Student]:
    """Returns an optimized queryset of active students with optional filtering."""
    qs = Student.objects.filter(is_active=True)
    if search_query:
        qs = qs.filter(last_name__icontains=search_query)
    return qs.order_by('last_name', 'first_name')
```
