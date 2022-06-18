from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user



class Roles:
    """
    The possible roles that can be stored in the database.
    The value of the string should match the value in the database.
    """
    # --- Primary roles
    # Each person can have zero to many of these.
    # Sysadmins can access everything everyone else can.
    CLIENT_ANALYST = 'client_analyst'
    CLIENT_STRATEGIST = 'client_strategist'

class Permissions:
    """
    Required roles to perform specific actions.

    Each permission should be a tuple of roles. Having any of the roles in the
    tuple constitutes having that permission. So for example:
        TEST = (Roles.X, Roles.Y, Roles.Z)
    This would allow anyone with X, Y or Z to have the TEST permission.

    If you'd like to require multiple roles for a permission, you can do that
    by placing multiple roles within another tuple. Consider the following:
        TEST = ((Roles.X, Roles.Y), Roles.Z)
    In this example, you either need to have both X and Y, or have Z.
    """
    # Bridge
    REPAIR_PERMISSIONS = (Roles.CLIENT_ANALYST,)
    
