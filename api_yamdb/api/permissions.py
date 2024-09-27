from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Создание/редактирование/удаление доступно
    администратору/суперпользователю, чтение для всех.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Для небезопасных методов проверяем, что пользователь аутентифицирован и является администратором
        return request.user.is_authenticated and request.user.is_admin


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class IsAuthorOrModeratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated):
            return True

        return (request.user.is_authenticated
                and (request.user.is_moderator or request.user.is_admin
                     or request.user.is_superuser))

    def has_object_permission(self, request, view, obj):

        if (request.method in permissions.SAFE_METHODS
                or obj.author == request.user):
            return True
        return (request.user.is_authenticated
                and (request.user.is_moderator or request.user.is_admin
                     or request.user.is_superuser))

