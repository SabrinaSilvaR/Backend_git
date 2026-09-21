from django.db import models

class ___ModelName___(models.Model):
    """
    ___ModelName___ domain model.
    """
    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '___model_name___s'
        ordering = ['-created_at']
        verbose_name = '___ModelName___'
        verbose_name_plural = '___ModelName___s'

    def __str__(self) -> str:
        return self.name
