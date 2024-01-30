from rest_framework import permissions


class isAdmin(permissions.BasePermission):
    """
    Разрешает доступ только администраторам.
    """
    def has_permission(self, request, view):
        return (
            not request.user.is_authenticated or request.user.role == 'admin'
        )


class IsAdminOrSuperUser(permissions.BasePermission):
    """
    Разрешает доступ только администраторам или суперпользователям.
    """
    def has_permission(self, request, view):
        return request.user.is_superuser or (
            request.user.is_authenticated and request.user.role == 'admin'
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает изменять данные только администратору.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'
