from rest_framework.permissions import BasePermission


class RolePermission(BasePermission):
    required_roles = ()

    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        return bool(
            user
            and user.is_authenticated
            and getattr(user, "role", None) in self.required_roles
        )
