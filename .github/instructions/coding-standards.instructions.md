---
applyTo: '**/*.py'
description: 'PEP 8 guidelines, naming conventions, type annotations, import ordering, and REST API conventions'
---

# Coding Standards

Rules and conventions for writing Python, Django, and Django REST Framework code in this repository.

## Python & PEP 8 Rules

- **Indentation:** 4 spaces per indentation level. Never use tabs in Python files.
- **Line length:** Keep lines around 88 to 100 characters.
- **Quotes:** Prefer single quotes for strings (`'hello'`), double quotes for docstrings (`"""Docstring"""`).
- **Naming Conventions:**
  - Classes: `PascalCase` (e.g. `StudentSerializer`, `CourseViewSet`, `RegistrationService`).
  - Functions & methods: `snake_case` (e.g. `create_student`, `validate_email`, `get_queryset`).
  - Variables: `snake_case` (e.g. `is_active`, `student_id`).
  - Constants: `SCREAMING_SNAKE_CASE` (e.g. `DEFAULT_PAGE_SIZE = 20`, `MAX_ATTEMPTS = 3`).
  - Protected / private attributes: prefixed with single underscore `_` (e.g. `_cached_value`).

## Import Ordering

Group imports in three distinct blocks separated by a single blank line:

```python
# 1. Standard library imports
import os
from datetime import date, datetime
from typing import Any

# 2. Third-party imports (Django, DRF, etc.)
from django.db import models, transaction
from rest_framework import serializers, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# 3. Local app imports
from .models import Student
from .selectors import get_active_students
from .services import register_student
```

## Type Hints & Annotations

- Annotate all function signatures:
  ```python
  def calculate_final_grade(scores: list[float], weights: list[float]) -> float:
      ...
  ```
- Use `| None` for optional types instead of `Optional[...]` (Python 3.10+ standard).

## Serializer Conventions

- **Explicit fields:**
  ```python
  # DO THIS:
  class StudentSerializer(serializers.ModelSerializer):
      class Meta:
          model = Student
          fields = ['id', 'first_name', 'last_name', 'email', 'created_at']
          read_only_fields = ['id', 'created_at']

  # NEVER DO THIS:
  class BadStudentSerializer(serializers.ModelSerializer):
      class Meta:
          model = Student
          fields = '__all__'  # Security risk: leaks internal fields
  ```

## Anti-Patterns to Avoid

- **Fat Views:** Putting 100+ lines of ORM queries and calculations inside `view.py`. Extract to `services.py` or `selectors.py`.
- **Catch-all Exceptions:** Catching bare `except:` or `except Exception: pass`. Catch specific errors.
- **N+1 ORM Queries:** Accessing foreign key fields inside a serialization loop without `select_related()`.
- **Hardcoded Secrets:** Writing database passwords or API keys directly in `settings.py`.
