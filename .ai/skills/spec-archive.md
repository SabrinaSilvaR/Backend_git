# Skill: Spec — Archive

Verify implementation, apply spec deltas to the living truth (`specs/specs/`), and move
the change folder to `specs/changes/archive/YYYY-MM-DD-<change-id>/`.

## When to use

After `/spec-implement` when all tasks in `tasks.md` are completed and tests pass.

## Procedure

1. **Verify Definition of Done:**
   - All tests pass (`python manage.py test apiGit`).
   - Migrations are generated and applied.
   - Code adheres to PEP 8 and project architecture.
2. **Apply Spec Deltas to Living Specs:**
   - For each capability in `specs/changes/<change-id>/specs/<capability>/spec.md`:
     - If capability is new: copy spec to `specs/specs/<capability>/spec.md` (removing delta headers).
     - If capability exists: apply `## ADDED` requirements, update `## MODIFIED` requirements, delete `## REMOVED` requirements in `specs/specs/<capability>/spec.md`.
3. **Archive Change:**
   - Move `specs/changes/<change-id>/` to `specs/changes/archive/YYYY-MM-DD-<change-id>/`.
4. **Summary:**
   - Report archived change to user in plain language.
