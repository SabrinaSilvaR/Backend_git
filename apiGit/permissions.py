from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):
    """Only users with role ADMIN (or superusers) can enter."""
    message = 'Solo los administradores pueden realizar esta acción.'

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.role == 'ADMIN' or user.is_superuser
