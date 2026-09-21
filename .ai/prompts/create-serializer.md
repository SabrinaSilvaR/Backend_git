# Prompt: Create DRF Serializer

Create a new Django REST Framework serializer in `apiGit/serializers.py`.

## Instructions

1. Use `serializers.ModelSerializer` for model representation, or `serializers.Serializer` for custom input forms.
2. Explicitly list `fields = [...]`; NEVER use `'__all__'`.
3. Set `read_only_fields = ['id', 'created_at']` where applicable.
4. Implement field validation methods `validate_<field>(self, value)` and/or object validation `validate(self, attrs)`.
5. If creating read vs write serializers, name them clearly (e.g. `StudentDetailSerializer` vs `StudentCreateSerializer`).
