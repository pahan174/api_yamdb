from rest_framework import permissions


class OwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        print(obj.author.role in ['moderator', 'admin', 'user'])
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or obj.author.role in ['moderator', 'admin']
            )



class AdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return (
            request.method in permissions.SAFE_METHODS
            or is_admin
        )
