from rest_framework.permissions import BasePermission, SAFE_METHODS

from users.models import CustomUser


class AdminPermission(BasePermission):

    def has_permission(self, request, view):
        if (request.user.is_authenticated and
                request.user.role != request.user.ADMIN):
            return True




