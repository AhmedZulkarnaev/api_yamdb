from rest_framework import permissions
from reviews.constants import ADMIN_ROLE


class IsAdmin(permissions.BasePermission):
    """
    Разрешает доступ только администраторам.
    """
    def has_permission(self, request, view):
        return (
            not request.user.is_authenticated
            or request.user.role == ADMIN_ROLE or request.user.is_staff
        )


class IsAdminOrSuperUser(permissions.BasePermission):
    """
    Разрешает доступ только администраторам или суперпользователям.
    """
    def has_permission(self, request, view):
        return request.user.is_superuser or (
            request.user.is_authenticated and request.user.role == 'admin'
        )
