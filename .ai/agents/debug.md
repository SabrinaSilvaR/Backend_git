# Django & DRF Debug Mode Instructions

> **Source of truth:** defer to [`AGENTS.md`](../../AGENTS.md) and the deep docs in
> [`.github/instructions/`](../../.github/instructions/).

You are in Debug Mode. Your mandate: diagnose, isolate, and resolve bugs, tracebacks, database query issues,
and serialization failures in this Django and DRF codebase.

## Diagnostic Protocol

1. **Capture the Traceback:** Identify the exact file, line number, and exception type (e.g., `ValidationError`, `IntegrityError`, `FieldDoesNotExist`, `KeyError`).
2. **Inspect Query Performance:** Check for N+1 queries. Look for missing `select_related()` or `prefetch_related()` calls.
3. **Verify Serializer Validation:** Inspect `serializer.errors` to see if fields failed validation or received invalid data types.
4. **Check Migrations:** Check `manage.py showmigrations` for unapplied or conflicting migrations.
5. **Reproduce via Test:** Write a failing test in `apiGit/tests/` reproducing the bug before modifying any implementation code.
6. **Fix & Verify:** Apply the minimal fix and confirm test passes with `.\vgit\Scripts\python.exe manage.py test apiGit`.
