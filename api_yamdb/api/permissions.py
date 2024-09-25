from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Создание/редактирование/удаление доступно
    администратору/суперпользователю, чтение для всех.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS or request.user.is_admin
        )


class AdminOnlyPermission(permissions.BasePermission):
    """Разрешение для администратора/суперпользователя."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAuthorUser(permissions.BasePermission):
    """
    Редактирование/удаление объекта доступно автору.
    """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsModeratorUser(permissions.BasePermission):
    """
    Редактирование/удаление объекта доступно модератору.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_moderator


class IsAuthenticatedForPut(permissions.BasePermission):
    """
    Разрешает доступ для всех пользователей к GET запросам,
    но требует аутентификации для PUT запросов.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method in ['patch', ] and request.user.is_moderator:
            return True
        return request.user and request.user.is_authenticated
