from rest_framework.permissions import SAFE_METHODS

from core.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from users.choices import UserTypeChoices


class IsOrganizationOwner(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.user_type == UserTypeChoices.ADMIN

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view,
                                             obj) and obj.organization == request.user.profile.organization


class IsOrganizationOwnerOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and (
                request.method in SAFE_METHODS or request.user.user_type == UserTypeChoices.ADMIN)

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj) and (
                request.method in SAFE_METHODS or obj.organization == request.user.profile.organization)
