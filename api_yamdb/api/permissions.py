from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            not request.user.is_authenticated
            or request.user.role == 'admin'
        )


class isSuperUser(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == 'moderator'
                     or request.user.is_staff
                     or request.user.is_superuser))
