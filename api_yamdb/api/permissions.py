from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsAdmin(BasePermission):
    """
    Разрешение, позволяет только администраторам создавать новых пользователей.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == 'admin'
        )


class IsModerator(BasePermission):
    """
    Разрешение, позволяет только администраторам создавать новых пользователей.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == 'moderator'
        )
