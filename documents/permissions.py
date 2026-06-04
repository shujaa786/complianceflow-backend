from accounts.constants import (
    ROLE_ADMIN,
    ROLE_APPROVER,
    ROLE_MANAGER,
    ROLE_VIEWER,
)
from shared.permissions.role import RolePermission


class IsAdmin(RolePermission):
    required_roles = (ROLE_ADMIN,)


class IsManager(RolePermission):
    required_roles = (ROLE_MANAGER,)


class IsApprover(RolePermission):
    required_roles = (ROLE_APPROVER,)


class IsViewer(RolePermission):
    required_roles = (ROLE_VIEWER,)
