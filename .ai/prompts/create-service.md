# Prompt: Create Django Service

Create a domain business logic function in `apiGit/services.py`.

## Instructions

1. Use pure Python functions with keyword-only arguments (`*`) and PEP 484 type annotations.
2. Use `@transaction.atomic` for multi-model writes or sensitive financial/state changes.
3. Handle domain validations by raising custom exceptions or `django.core.exceptions.ValidationError`.
4. Trigger external side effects (emails, notifications, third-party APIs) cleanly inside the service.
