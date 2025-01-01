from rest_framework import decorators, parsers, response, status, viewsets

from . import permissions
from .models import (CustomUser, UserProfile,Certification,Course,ForumPost,Exam,Enrollment,
                     Lesson, UserComplaint,Review)
from .serializers import (CustomUserSerializer, UserProfileSerializer, 
                          CertificationSerializer,CourseSerializer,
                          EnrollmentSerializer,ExamSerializer,
                          ForumPostSerializer,BaseModelSerializer,LessonSerializer,UserComplaintSerializer,ReviewSerializer)
from django.utils import timezone
from datetime import timedelta
from rest_framework import serializers


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.CustomUserPermission,)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.UserProfilePermission,)

    @decorators.action(
        detail=True,
        methods=["put"],
        name="Upload banner",
        parser_classes=[parsers.FileUploadParser],
    )
    def upload_banner(self, request, pk=None):
        """
        Upload banner using a PUT request.

        Use the Content-Type header to specify the file type, and the
        Content-Disposition header to specify the filename, for example:

            Content-Type: image/png
            Content-Disposition: attachment; filename=screenshot.png
        """

        obj = self.get_object()
        file = request.data.get("file")
        if not file:
            return response.Response(
                {"error": "Missing content"},
                status=status.HTTP_404_BAD_REQUEST,
            )

        obj.banner.save(file.name, file, save=True)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @decorators.action(
        detail=True,
        methods=["put"],
        name="Upload profile_picture",
        parser_classes=[parsers.FileUploadParser],
    )
    def upload_profile_picture(self, request, pk=None):
        """
        Upload profile_picture using a PUT request.

        Use the Content-Type header to specify the file type, and the
        Content-Disposition header to specify the filename, for example:

            Content-Type: image/png
            Content-Disposition: attachment; filename=screenshot.png
        """

        obj = self.get_object()
        file = request.data.get("file")
        if not file:
            return response.Response(
                {"error": "Missing content"},
                status=status.HTTP_404_BAD_REQUEST,
            )

        obj.profile_picture.save(file.name, file, save=True)
        return response.Response(status=status.HTTP_204_NO_CONTENT)
class CertificationViewSet(viewsets.ModelViewSet):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    permission_classes = (permissions.CertificationPermission,)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (permissions.CoursePermission,)

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (permissions.LessonPermission,)
    @decorators.action(
        detail=True,
        methods=["put"],
        name="Upload lesson picture",
        parser_classes=[parsers.FileUploadParser],
    )
    def upload_lesson_picture(self, request, pk=None):
        """
        Upload profile_picture using a PUT request.

        Use the Content-Type header to specify the file type, and the
        Content-Disposition header to specify the filename, for example:

            Content-Type: image/png
            Content-Disposition: attachment; filename=screenshot.png
        """

        obj = self.get_object()
        file = request.data.get("file")
        if not file:
            return response.Response(
                {"error": "Missing content"},
                status=status.HTTP_404_BAD_REQUEST,
            )

        obj.profile_picture.save(file.name, file, save=True)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = (permissions.EnrollmentPermission,)

class UserComplaintViewSet(viewsets.ModelViewSet):
    queryset = UserComplaint.objects.all()
    serializer_class = UserComplaintSerializer
    permission_classes = (permissions.UserComplaintPermission,)
    def perform_create(self, serializer):
        user = self.request.user
        three_days_ago = timezone.now() - timedelta(days=3)

        recent_complaints = UserComplaint.objects.filter(user=user, created_at__gte=three_days_ago)
        
        if recent_complaints.exists():
            raise serializers.ValidationError("You can only submit a complaint once every 3 days.")

        serializer.save(user=user)


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = (permissions.ExamPermission,)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (permissions.ReviewPermission,)


class ForumPostViewSet(viewsets.ModelViewSet):
    queryset = ForumPost.objects.all()
    serializer_class = ForumPostSerializer
    permission_classes = (permissions.ForumPostPermission,)
