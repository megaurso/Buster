from rest_framework import permissions
from rest_framework.views import Request, View
from users.models import User


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, req: Request, view: View, obj: User) -> bool:
        return obj == req.user or req.user.is_employee
