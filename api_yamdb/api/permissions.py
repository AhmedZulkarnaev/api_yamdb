from rest_framework import permissions
from reviews.constants import ADMIN_ROLE, MODERATOR_ROLE


class IsAdmin(permissions.BasePermission):
    """
    Разрешает доступ только администраторам.
    """
    def has_permission(self, request, view):
        return (
            not request.user.is_authenticated
            or request.user.role == ADMIN_ROLE or request.user.is_staff
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает изменять данные только администратору.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and request.user.role == ADMIN_ROLE)


class IsAuthorModeratorAdminOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Разрешает изменения только авторам, модераторам и администраторам."""

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role in [MODERATOR_ROLE, ADMIN_ROLE]
                or obj.author == request.user)
