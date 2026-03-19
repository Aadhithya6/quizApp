from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to users with the ADMIN role.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'ADMIN')

class IsModeratorUser(permissions.BasePermission):
    """
    Allows access only to users with the MODERATOR role.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'MODERATOR')

class IsAdminOrModerator(permissions.BasePermission):
    """
    Allows access only to users with ADMIN or MODERATOR roles.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['ADMIN', 'MODERATOR']
        )

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` or `created_by` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner` or `created_by`.
        owner = getattr(obj, 'created_by', getattr(obj, 'user', None))
        return owner == request.user

class IsAuthenticatedUser(permissions.BasePermission):
    """
    Allows access to any authenticated user.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
