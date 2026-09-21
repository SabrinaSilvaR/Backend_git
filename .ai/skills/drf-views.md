# Skill: DRF Views, ViewSets, and Routers

Guidelines for organizing API endpoints, handling requests, and configuring routes.

## Choosing the Right View Pattern

1. **`ModelViewSet` (Full CRUD):**
   - Best for standard resource management with list, retrieve, create, update, and destroy operations.
   - Use `rest_framework.routers.DefaultRouter` to automatically generate standard REST URL routes.
   - Add custom endpoint actions with the `@action` decorator:
     ```python
     @action(detail=True, methods=['post'], url_path='activate')
     def activate(self, request, pk=None):
         ...
     ```

2. **`GenericAPIView` with Mixins:**
   - Best when only specific operations are supported (e.g., `ListCreateAPIView`, `RetrieveUpdateAPIView`).

3. **`APIView`:**
   - Best for specialized or RPC-like procedural endpoints (e.g., triggering a calculation, executing an export, complex authentication exchange).

## Keep Views Thin

- Views should only:
  1. Authenticate & authorize the caller (`permission_classes`).
  2. Parse and validate input data with a Serializer (`serializer.is_valid(raise_exception=True)`).
  3. Invoke domain logic from `services.py` or `selectors.py`.
  4. Return an appropriate HTTP response (`status=status.HTTP_201_CREATED`, `status=status.HTTP_200_OK`, etc.).

## Example ViewSet:

```python
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Student
from .serializers import StudentSerializer
from .selectors import get_active_students
from .services import create_student

class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_active_students()

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        student = create_student(**validated_data)
        serializer.instance = student
```
