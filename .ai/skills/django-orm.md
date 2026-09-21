# Skill: Django ORM Best Practices

Guidelines and patterns for designing models, relationships, and queries using the Django Object-Relational Mapper.

## Model Design Principles

1. **Explicit Field Definitions:**
   - Always define `null` and `blank` intentionally. For string fields (`CharField`, `TextField`), use `blank=True` instead of `null=True` unless uniqueness is required.
   - For foreign keys, always provide an explicit, descriptive `related_name` in snake_case (e.g., `related_name='enrollments'`).
   - Specify `on_delete` intentionally: prefer `models.PROTECT` or `models.CASCADE` depending on business domain logic.

2. **Meta Options:**
   - Always define `ordering`, `verbose_name`, `verbose_name_plural`, and custom constraints / indexes under `class Meta:`.
   - Use `models.UniqueConstraint` and `models.CheckConstraint` over deprecated `unique_together`.

3. **String Representation:**
   - Always implement `def __str__(self) -> str:` returning a human-readable identifier.

4. **Example Model:**
   ```python
   from django.db import models

   class Student(models.Model):
       first_name = models.CharField(max_length=100)
       last_name = models.CharField(max_length=100)
       email = models.EmailField(unique=True)
       enrollment_date = models.DateField(auto_now_add=True)
       is_active = models.BooleanField(default=True)

       class Meta:
           db_table = 'students'
           ordering = ['-enrollment_date', 'last_name']
           verbose_name = 'Student'
           verbose_name_plural = 'Students'

       def __str__(self) -> str:
           return f"{self.first_name} {self.last_name} ({self.email})"
   ```

## Query Optimization & Anti-Patterns

- **N+1 Queries:** Never iterate over related models without eager loading:
  - Use `select_related('foreign_key_field')` for `ForeignKey` and `OneToOneField`.
  - Use `prefetch_related('many_to_many_or_reverse_fk')` for `ManyToManyField` and reverse lookups.
- **Bulk Operations:** Use `bulk_create()` and `bulk_update()` when handling lists of entities instead of saving in a loop.
- **Transactions:** Use `from django.db import transaction` with `with transaction.atomic():` or `@transaction.atomic` for multi-step mutations.
