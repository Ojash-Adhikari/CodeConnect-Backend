from rest_framework.permissions import SAFE_METHODS

from users.choices import UserTypeChoices
from rest_framework import permissions

    
class IsOwnUser(permissions.BasePermission):
    """
    Custom permission to only allow a user to update their own data.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is trying to access their own data
        return obj == request.user
