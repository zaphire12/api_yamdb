from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешения для пользователей."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == 'admin' or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == 'admin' or request.user.is_staff
        )
