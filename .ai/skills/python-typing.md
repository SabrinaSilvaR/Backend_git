# Skill: Python Typing & Code Quality

Standards for type hints, docstrings, and clean Python code.

## Type Hints (PEP 484)

- Annotate all function parameters and return types.
- Use built-in generics in Python 3.10+ (`list[str]`, `dict[str, Any]`, `str | None`).
- Use `from typing import Any, Protocol` when necessary.

```python
from typing import Any
from django.db.models import QuerySet
from .models import Student

def filter_students_by_domain(
    queryset: QuerySet[Student],
    domain: str = "inacap.cl"
) -> QuerySet[Student]:
    """Filter students whose email belongs to a specific domain."""
    return queryset.filter(email__endswith=f"@{domain}")
```

## Anti-Patterns to Avoid

- Avoid using bare `except:`; always catch specific exceptions (`except Student.DoesNotExist:` or `except ValidationError:`).
- Avoid `type: ignore` comments unless dealing with dynamic Django ORM attributes that type checkers cannot resolve.
- Avoid wildcard imports (`from .models import *`); explicitly import classes and functions.
