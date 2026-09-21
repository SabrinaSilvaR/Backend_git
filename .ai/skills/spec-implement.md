# Skill: Spec — Implement

Execute the change's task list with a test → implement → migrate → verify loop, reusing the template's
existing task prompts.

## When to use

After `/spec-tasks`. Input: `specs/changes/<change-id>/tasks.md`.

## Stack quality gates — Python + Django + DRF

The implement loop runs against the local virtualenv toolchain:

```bash
# Run tests
.\vgit\Scripts\python.exe manage.py test apiGit

# Create and apply migrations
.\vgit\Scripts\python.exe manage.py makemigrations
.\vgit\Scripts\python.exe manage.py migrate

# Check for schema/model integrity
.\vgit\Scripts\python.exe manage.py check
```

## Procedure

Work tasks **in order**. For each task:

1. **Red** — write or adjust tests in `apiGit/tests/` (`test_models.py`, `test_serializers.py`, `test_views.py`) using `rest_framework.test.APITestCase`. Run `manage.py test` and verify test fails as expected.
2. **Green** — implement the minimal code to satisfy the test, referencing matching prompts:
   - Models → `.ai/prompts/create-model.md`
   - Serializers → `.ai/prompts/create-serializer.md`
   - Views / ViewSets → `.ai/prompts/create-viewset.md`
   - Services → `.ai/prompts/create-service.md`
   - Tests → `.ai/prompts/create-test.md`
   - Migrations → `.ai/prompts/create-migration.md`
3. **Migrate & verify** — run `makemigrations` and `migrate` if models changed. Run `manage.py test apiGit` to ensure all tests pass cleanly.
4. **Conform to conventions** (`AGENTS.md` + `coding-standards`): PEP 8, snake_case, type hints, thin views, explicit serializer fields, no N+1 queries.
5. **Check off the task** in `tasks.md` and proceed to the next.

## Output

- Summary of files changed, migrations created, and test suite execution results.
- **Next step:** `/spec-archive` once all tasks are checked.
