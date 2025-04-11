from rest_framework import decorators, parsers, response, status, viewsets

from . import permissions
from .models import (CustomUser, UserProfile,Certification,Course,ForumPost,Exam,Enrollment,
                     Lesson, UserComplaint,Review,Notification, Activity)
from .serializers import (CustomUserSerializer, UserProfileSerializer, 
                          CertificationSerializer,CourseSerializer,
                          EnrollmentSerializer,ExamSerializer,
                          ForumPostSerializer,BaseModelSerializer,LessonSerializer,
                          UserComplaintSerializer,ReviewSerializer,CountrySerializer,NotificationSerializer, ActivitySerializer)
from django.utils import timezone
from datetime import timedelta
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import ListAPIView
from cities_light.models import Country
from rest_framework.response import Response

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.CustomUserPermission,)

class CountryListView(ListAPIView):
    queryset = Country.objects.all().order_by('name_ascii') 
    serializer_class = CountrySerializer
    pagination_class = None

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
                status=status.HTTP_400_BAD_REQUEST,
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
                status=status.HTTP_400_BAD_REQUEST,
            )

        obj.profile_picture.save(file.name, file, save=True)
        return response.Response(status=status.HTTP_204_NO_CONTENT)
class CertificationViewSet(viewsets.ModelViewSet):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    permission_classes = (permissions.CertificationPermission,)


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = (permissions.CoursePermission,)

    def get_queryset(self):
        user = self.request.user
        if user.user_type.upper() == "ADMIN": 
            return Course.objects.all()
        return Course.objects.filter(is_activated=True)

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = (permissions.LessonPermission,)
    @decorators.action(
    detail=True,
    methods=["put"],
    name="Upload lesson picture",
    parser_classes=[MultiPartParser, FormParser],
    )
    def upload_lesson_picture(self, request, pk=None):
        obj = self.get_object()
        file = request.FILES.get("picture")  # <-- Grab from FILES and use 'picture' to match frontend
        if not file:
            return response.Response(
                {"error": "Missing content"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        obj.picture.save(file.name, file, save=True)
        return response.Response(
            {"picture_url": obj.picture.url},  # Nice to return the URL
            status=status.HTTP_200_OK,
        )
    @decorators.action(detail=True, methods=['put'])
    def upload_lesson_video(self, request, pk=None):
        lesson = self.get_object()
        if 'video' in request.FILES:
            lesson.video = request.FILES['video']
            lesson.save()

            # Construct absolute URL for frontend usage
            video_url = request.build_absolute_uri(lesson.video.url)
            
            return response.Response({'video_url': video_url}, status=status.HTTP_200_OK)

        return response.Response({'error': 'No video uploaded'}, status=status.HTTP_400_BAD_REQUEST)
    
class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = (permissions.EnrollmentPermission,)

    def create(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course')

        # Check if already enrolled
        if Enrollment.objects.filter(user=user, course_id=course_id).exists():
            return Response(
                {'detail': 'You are already enrolled in this course.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (permissions.NotificationPermission,)

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes= (permissions.ActivityPermission,)    


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
    serializer_class = ReviewSerializer
    permission_classes = (permissions.ReviewPermission,)

    def get_queryset(self):
        """
        Optionally restricts the returned reviews to a given course,
        by filtering against a `course` query parameter in the URL.
        """
        queryset = Review.objects.all()
        course_id = self.request.query_params.get('course', None)
        created_by_id = self.request.query_params.get('created_by', None)
        if course_id is not None:
            queryset = queryset.filter(course_id=course_id)
        if created_by_id is not None:
            queryset = queryset.filter(created_by_id=created_by_id)
            
        return queryset

class ForumPostViewSet(viewsets.ModelViewSet):
    queryset = ForumPost.objects.all()
    serializer_class = ForumPostSerializer
    permission_classes = (permissions.ForumPostPermission,)
