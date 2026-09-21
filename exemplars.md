# Code Exemplars

This document identifies high-quality, representative code patterns for this Python + Django + Django REST Framework repository.
These exemplars demonstrate our architectural layers and coding standards.

## Architecture Layer Exemplars

### 1. Data Layer: Django ORM Model (`apiGit/models.py`)

**Pattern**: Domain model with explicit typing, clean Meta options, and string representation.

```python
from django.db import models

class Student(models.Model):
    """
    Represents an enrolled student in the institution.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'students'
        ordering = ['last_name', 'first_name']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.rut})"
```

---

### 2. Validation & Serialization Layer (`apiGit/serializers.py`)

**Pattern**: ModelSerializer with explicit fields, read-only guarantees, and validation methods.

```python
from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'full_name', 'rut', 'email', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_full_name(self, obj: Student) -> str:
        return f"{obj.first_name} {obj.last_name}"

    def validate_rut(self, value: str) -> str:
        clean_rut = value.replace('.', '').replace('-', '').upper().strip()
        if len(clean_rut) < 8 or len(clean_rut) > 9:
            raise serializers.ValidationError("Invalid RUT format.")
        return clean_rut

    def validate_email(self, value: str) -> str:
        return value.lower().strip()
```

---

### 3. Business Service Layer (`apiGit/services.py`)

**Pattern**: Domain service function with atomic transaction and type hints.

```python
from django.db import transaction
from .models import Student

@transaction.atomic
def register_student(
    *,
    first_name: str,
    last_name: str,
    rut: str,
    email: str
) -> Student:
    """
    Registers a student and executes any associated domain side-effects.
    """
    return Student.objects.create(
        first_name=first_name.strip(),
        last_name=last_name.strip(),
        rut=rut.strip(),
        email=email.lower().strip(),
        is_active=True,
    )
```

---

### 4. Query Selector Layer (`apiGit/selectors.py`)

**Pattern**: Pre-optimized read queries avoiding N+1 bottlenecks.

```python
from django.db.models import QuerySet
from .models import Student

def get_active_students(*, rut: str | None = None) -> QuerySet[Student]:
    """
    Retrieves active students, optionally filtered by RUT.
    """
    qs = Student.objects.filter(is_active=True)
    if rut:
        qs = qs.filter(rut__icontains=rut)
    return qs.order_by('last_name', 'first_name')
```

---

### 5. API Controller Layer (`apiGit/views.py`)

**Pattern**: Thin ModelViewSet delegating queries and mutations.

```python
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Student
from .serializers import StudentSerializer
from .selectors import get_active_students
from .services import register_student

class StudentViewSet(viewsets.ModelViewSet):
    """
    RESTful API endpoint for managing students.
    """
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        rut_filter = self.request.query_params.get('rut')
        return get_active_students(rut=rut_filter)

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        student = register_student(**validated_data)
        serializer.instance = student
```
