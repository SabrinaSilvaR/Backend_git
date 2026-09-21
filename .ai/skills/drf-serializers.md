# Skill: Django REST Framework Serializers

Guidelines and patterns for creating robust, validated serializers with DRF.

## Core Principles

1. **Explicit Fields:**
   - Never use `fields = '__all__'`. Explicitly list fields to prevent accidental exposure of sensitive internal attributes (like password hashes or internal status flags).
   - Define `read_only_fields = ['id', 'created_at', 'updated_at']` where appropriate.

2. **Validation Rules:**
   - **Field-level validation:** Use `validate_<field_name>(self, value)`:
     ```python
     def validate_grade(self, value: float) -> float:
         if not (1.0 <= value <= 7.0):
             raise serializers.ValidationError("Grade must be between 1.0 and 7.0.")
         return value
     ```
   - **Cross-field validation:** Use `validate(self, attrs: dict) -> dict`:
     ```python
     def validate(self, attrs: dict) -> dict:
         if attrs.get('end_date') and attrs.get('start_date'):
             if attrs['end_date'] < attrs['start_date']:
                 raise serializers.ValidationError({"end_date": "End date cannot be earlier than start date."})
         return attrs
     ```

3. **Separation of Read and Write Serializers:**
   - When output representations differ significantly from input payloads (e.g., nested objects on read vs. foreign key IDs on write), create distinct serializers: `StudentReadSerializer` and `StudentWriteSerializer`.

4. **Serializer Pattern Example:**
   ```python
   from rest_framework import serializers
   from .models import Student

   class StudentSerializer(serializers.ModelSerializer):
       full_name = serializers.SerializerMethodField()

       class Meta:
           model = Student
           fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 'enrollment_date', 'is_active']
           read_only_fields = ['id', 'enrollment_date']

       def get_full_name(self, obj: Student) -> str:
           return f"{obj.first_name} {obj.last_name}"

       def validate_email(self, value: str) -> str:
           return value.lower().strip()
   ```
