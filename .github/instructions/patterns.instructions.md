---
applyTo: '**/*.py'
description: 'Copy-paste code recipes for Django models, DRF serializers, ViewSets, services, selectors, permissions, and tests'
---

# Patterns & Recipes

Standard reference patterns for development in this repository.

## 1. Model Pattern (`models.py`)

```python
from django.db import models

class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    credits = models.PositiveIntegerField(default=4)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'courses'
        ordering = ['code']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"
```

## 2. Serializer Pattern (`serializers.py`)

```python
from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'code', 'name', 'description', 'credits', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_code(self, value: str) -> str:
        code_clean = value.strip().upper()
        if len(code_clean) < 3:
            raise serializers.ValidationError("Course code must be at least 3 characters.")
        return code_clean

    def validate_credits(self, value: int) -> int:
        if value < 1:
            raise serializers.ValidationError("Credits must be a positive number.")
        return value
```

## 3. Service Pattern (`services.py`)

```python
from django.db import transaction
from .models import Course

@transaction.atomic
def create_course(*, code: str, name: str, description: str = '', credits: int = 4) -> Course:
    """Domain service to safely create a new course."""
    return Course.objects.create(
        code=code.strip().upper(),
        name=name.strip(),
        description=description.strip(),
        credits=credits,
        is_active=True,
    )
```

## 4. Selector Pattern (`selectors.py`)

```python
from django.db.models import QuerySet
from .models import Course

def get_active_courses(*, search: str | None = None) -> QuerySet[Course]:
    """Retrieve active courses with optional search."""
    qs = Course.objects.filter(is_active=True)
    if search:
        qs = qs.filter(name__icontains=search)
    return qs.order_by('code')
```

## 5. ViewSet Pattern (`views.py`)

```python
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Course
from .serializers import CourseSerializer
from .selectors import get_active_courses
from .services import create_course

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        search = self.request.query_params.get('search')
        return get_active_courses(search=search)

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        course = create_course(**validated_data)
        serializer.instance = course
```

## 6. Test Pattern (`tests/test_views.py`)

```python
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apiGit.models import Course

class CourseAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin_test', password='secretpassword')
        self.course = Course.objects.create(code='CS101', name='Intro to Programming', credits=4)
        self.list_url = reverse('course-list')

    def test_unauthenticated_cannot_access(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_can_list_courses(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_invalid_course_code_fails(self):
        self.client.force_authenticate(user=self.user)
        payload = {'code': 'A', 'name': 'Bad Code', 'credits': 4}
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('code', response.data)
```
