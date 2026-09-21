# Prompt: Create Django Model

Create a new Django ORM model adhering to repository standards.

## Instructions

1. Define model in `apiGit/models.py` (or specific app's `models.py`).
2. Include PEP 484 type hints where appropriate.
3. Define `verbose_name`, `verbose_name_plural`, `ordering`, and `db_table` in `class Meta:`.
4. Define explicit `related_name` for all `ForeignKey` and `ManyToManyField`.
5. Implement `def __str__(self) -> str:`.
6. Run `.\vgit\Scripts\python.exe manage.py makemigrations` to generate migration.
7. Run `.\vgit\Scripts\python.exe manage.py migrate` to apply changes.
