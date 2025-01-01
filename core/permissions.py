from rest_framework import permissions


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
    
class LessonPermission(permissions.BasePermission):
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
    
class EnrollmentPermission(permissions.BasePermission):
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
