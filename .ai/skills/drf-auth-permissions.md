# Skill: DRF Authentication & Permissions

Patterns for securing endpoints and managing authorization.

## Authentication Schemes

- **SessionAuthentication:** Best for browser-based interaction and Django Admin.
- **TokenAuthentication / JWT (e.g. SimpleJWT):** Best for SPA or mobile client applications.

## Permission Classes

Use DRF built-in permissions or compose custom permissions:
- `AllowAny`: Public read-only endpoints (e.g. health check, public documentation).
- `IsAuthenticated`: Authenticated users only.
- `IsAdminUser`: Staff / admin accounts only.

## Custom Permissions (`BasePermission`)

Always implement `has_permission` (for the endpoint view) and/or `has_object_permission` (for specific instances):

```python
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from django.views import View

class IsOwnerOrReadOnly(BasePermission):
    """Allow full access to owners, but read-only access to others."""

    def has_object_permission(self, request: Request, view: View, obj: any) -> bool:
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user
```
