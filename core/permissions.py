from rest_framework import permissions
from users.choices import UserTypeChoices

class CustomUserPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # anyone can read
            return True

        if view.action in ["update", "partial_update"]:
            # only the admins can update
            return request.user.is_authenticated and request.user.is_superuser

        if view.action == "destroy":
            # only the admins can delete
            return request.user.is_authenticated and request.user.is_superuser

        return False

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # anyone can list objects
            return True

        if view.action == "create":
            # any authenticated user can create
            return request.user.is_authenticated

        return True


class UserProfilePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # anyone can read
            return True

        if view.action in [
            "update",
            "partial_update",
            "upload_banner",
            "upload_profile_picture",
        ]:
            # only the admins can update
            return request.user.is_authenticated and request.user.is_superuser

        if view.action == "destroy":
            # only the admins can delete
            return request.user.is_authenticated and request.user.is_superuser

        return False

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # anyone can list objects
            return True

        if view.action == "create":
            # any authenticated user can create
            return request.user.is_authenticated

        return True

class CertificationPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # anyone can read
            return True

        if view.action in ["update", "partial_update"]:
            # only the admins can update
            return request.user.is_authenticated and request.user.is_superuser

        if view.action == "destroy":
            # only the admins can delete
            return request.user.is_authenticated and request.user.is_superuser

        return False

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # anyone can list objects
            return True

        if view.action == "create":
            # any authenticated user can create
            return request.user.is_authenticated

        return True
    
class CoursePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow read access to anyone

        if view.action == "create":
            # Ensure user is authenticated and is an ADMIN or superuser
            return request.user.is_authenticated and (
                request.user.is_superuser or request.user.user_type.upper() == "ADMIN"
            )

        return False  # Deny all other cases

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow read access

        if view.action in ["update", "partial_update"]:
            return request.user.is_authenticated and (
                request.user.is_superuser or request.user.user_type.upper() == "ADMIN"
            )

        if view.action == "destroy":
            return request.user.is_authenticated and (
                request.user.is_superuser or request.user.user_type.upper() == "ADMIN"
            )

        return False

class NotificationPermission(permissions.BasePermission):
    """
    Custom permission to allow only Admins or Superusers to update notifications.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow read access to anyone
        
        if view.action in ["update", "partial_update"]:
            return request.user.is_authenticated and (
                request.user.is_superuser or request.user.user_type.upper() == "ADMIN"
            )

        return False  # Deny all other cases

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow read access
        
        if view.action in ["update", "partial_update"]:
            return request.user.is_authenticated and (
                request.user.is_superuser or request.user.user_type.upper() == "ADMIN"
            )

        return False

class LessonPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if view.action in ["update", "partial_update", "upload_lesson_picture", "upload_lesson_video"]:
            # only admins can update or upload files
            return request.user.is_authenticated and (
                request.user.is_superuser or request.user.user_type.upper() == "ADMIN"
            )

        if view.action == "destroy":
            return request.user.is_authenticated and (
                request.user.is_superuser or request.user.user_type.upper() == "ADMIN"
            )

        return False

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated and (
                request.user.is_superuser or request.user.user_type.upper() in ["USER", "ADMIN"]
            )

        if view.action in ["create", "upload_lesson_picture", "upload_lesson_video"]:
            return request.user.is_authenticated and (
                request.user.is_superuser or request.user.user_type.upper() == "ADMIN"
            )

        return True

class ActivityPermission(permissions.BasePermission):
    """
    Custom permission to allow only admins to view activities.
    """
    
    def has_permission(self, request, view):
        return request.user and (request.user.is_superuser or request.user.user_type.upper() == "ADMIN")


class EnrollmentPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow GET only if the user owns the object
        if request.method in permissions.SAFE_METHODS:
            return obj.user == request.user

        # Only admins can update or delete
        if view.action in ["update", "partial_update", "destroy"]:
            return request.user.is_authenticated and (
                request.user.is_superuser or request.user.user_type.upper() == "ADMIN"
            )

        return False

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # Allow access; object-level check will restrict to their own data
            return request.user.is_authenticated

        if view.action == "create":
            # Any authenticated user can create
            return request.user.is_authenticated

        # Deny other actions unless covered above
        return False

class UserComplaintPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # anyone can read
            return True

        if view.action in ["update", "partial_update"]:
            # only the admins can update
            return request.user.is_authenticated and request.user.is_superuser

        if view.action == "destroy":
            # only the admins can delete
            return request.user.is_authenticated and request.user.is_superuser

        return False

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # anyone can list objects
            return True

        if view.action == "create":
            # any authenticated user can create
            return request.user.is_authenticated

        return True
    
class ReviewPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Anyone can view the review
            return True
        
        if request.user.is_superuser:
            # Admins can perform any action (CRUD) on any review
            return True
        
        # If the user is trying to update or delete a review, ensure it's their own review
        if view.action in ["update", "partial_update", "destroy"]:
            return obj.user == request.user

        return False

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # Anyone can list objects or view individual reviews
            return True

        if view.action == "create":
            # Any authenticated user can create a review
            return request.user.is_authenticated

        return True

class ExamPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # anyone can read
            return True

        if view.action in ["update", "partial_update"]:
            # only the admins can update
            return request.user.is_authenticated and request.user.is_superuser

        if view.action == "destroy":
            # only the admins can delete
            return request.user.is_authenticated and request.user.is_superuser

        return False

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # anyone can list objects
            return True

        if view.action == "create":
            # any authenticated user can create
            return request.user.is_authenticated

        return True


class ForumPostPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # anyone can read
            return True

        if view.action in ["update", "partial_update"]:
            # only the admins can update
            return request.user.is_authenticated and request.user.is_superuser

        if view.action == "destroy":
            # only the admins can delete
            return request.user.is_authenticated and request.user.is_superuser

        return False

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # anyone can list objects
            return True

        if view.action == "create":
            # any authenticated user can create
            return request.user.is_authenticated

        return True
