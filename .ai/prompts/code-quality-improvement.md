# Prompt: Code Quality Improvement

Review and improve Python code quality, typing, and PEP 8 conformance.

## Instructions

1. Check for unused imports and remove them.
2. Ensure all function signatures include type hints (`arg: Type -> ReturnType`).
3. Check for N+1 queries in views and serializers; introduce `select_related` or `prefetch_related`.
4. Ensure serializers do not use `fields = '__all__'`.
5. Run tests: `.\vgit\Scripts\python.exe manage.py test apiGit` to verify no regressions.
