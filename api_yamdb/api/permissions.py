from rest_framework import permissions


class IsAuthorModeratorAdminOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Разрешает изменения только авторам, модераторам и администраторам."""

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS or
                request.user.role in ['moderator', 'admin'] or
                obj.author == request.user)
