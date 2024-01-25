from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'moderator'


class IsAdminOrReadOnly(BasePermission):
    """
    Разрешение, позволяет только администраторам создавать новых пользователей.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == 'admin'
        )
