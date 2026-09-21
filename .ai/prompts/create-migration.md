# Prompt: Create and Run Django Migration

Generate and apply safe Django schema migrations.

## Instructions

1. Verify model definitions in `apiGit/models.py`.
2. Generate migration: `.\vgit\Scripts\python.exe manage.py makemigrations`.
3. Inspect generated migration in `apiGit/migrations/` for correctness and non-destructive operations.
4. Apply migration: `.\vgit\Scripts\python.exe manage.py migrate`.
5. Verify schema with: `.\vgit\Scripts\python.exe manage.py showmigrations`.
