# Skill: Spec — Tasks

Break down a change into ordered, atomic, test-first tasks (`specs/changes/<change-id>/tasks.md`).

## When to use

After `/spec-propose` (and `/spec-design` if needed). Input: `proposal.md` + `design.md`.

## Procedure

1. **Order tasks logically (test-first):**
   - Task 1: Draft unit/integration tests for models, serializers, or services (Red phase).
   - Task 2: Implement models, generate migrations, apply migrations (`makemigrations` / `migrate`).
   - Task 3: Implement serializers and validation logic.
   - Task 4: Implement services / business logic functions.
   - Task 5: Implement API Views or ViewSets and register URLs.
   - Task 6: Run tests and verify all pass (Green phase).
   - Task 7: Refactor, type-check, and review code quality.
2. **Save tasks list:** In `specs/changes/<change-id>/tasks.md` using `.ai/templates/tasks.template.md`.
3. **Next step:** `/spec-implement`.
