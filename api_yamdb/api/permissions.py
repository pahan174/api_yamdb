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
        return obj.author == request.user


class AdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return (
            request.method in permissions.SAFE_METHODS
            or is_admin
        )


class IsAuthorOrModerOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if (request.method in permissions.SAFE_METHODS or
                request.user.is_authenticated):
            return True

    def has_object_permission(self, request, view, obj):
        if not (request.method in permissions.SAFE_METHODS):
            return request.user.is_authenticated and (
                request.user.role in ['admin', 'moderator']
                or (request.user == obj.author)
            )
        return True
