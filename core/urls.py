from django.urls import path, include
from rest_framework import routers

from .views import (CustomUserViewSet, UserProfileViewSet, CertificationViewSet, CourseViewSet,
                    EnrollmentViewSet, ExamViewSet, ForumPostViewSet,LessonViewSet,UserComplaintViewSet,ReviewViewSet)

app_name = "core"


urlpatterns = [
    path("core/custom-user/", CustomUserViewSet.as_view({'get': 'list', 'post': 'create'}), name='customuser-list'),
    path("core/custom-user/<int:pk>/", CustomUserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='customuser-detail'),
    
    path("core/user-profile/", UserProfileViewSet.as_view({'get': 'list', 'post': 'create'}), name='userprofile-list'),
    path("core/user-profile/<int:pk>/", UserProfileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='userprofile-detail'),

    path("core/certification/", CertificationViewSet.as_view({'get': 'list', 'post': 'create'}), name='certification-list'),
    path("core/certification/<int:pk>/", CertificationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='certification-detail'),

    path("core/course/", CourseViewSet.as_view({'get': 'list', 'post': 'create'}), name='course-list'),
    path("core/course/<int:pk>/", CourseViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='course-detail'),

    path("core/course/lesson", LessonViewSet.as_view({'get': 'list', 'post': 'create'}), name='lesson-list'),
    path("core/course/lesson/<int:pk>/", LessonViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='lesson-detail'),


    path("core/enrollment/", EnrollmentViewSet.as_view({'get': 'list', 'post': 'create'}), name='enrollment-list'),
    path("core/enrollment/<int:pk>/", EnrollmentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='enrollment-detail'),

    path("core/complaints/", UserComplaintViewSet.as_view({'get': 'list', 'post': 'create'}), name='complaint-list'),
    path("core/complaints/<int:pk>/", UserComplaintViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='complaint-detail'),

    path("core/review/", ReviewViewSet.as_view({'get': 'list', 'post': 'create'}), name='review-list'),
    path("core/review/<int:pk>/", ReviewViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='review-detail'),

    path("core/exam/", ExamViewSet.as_view({'get': 'list', 'post': 'create'}), name='exam-list'),
    path("core/exam/<int:pk>/", ExamViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='exam-detail'),

    path("core/forum-post/", ForumPostViewSet.as_view({'get': 'list', 'post': 'create'}), name='forumpost-list'),
    path("core/forum-post/<int:pk>/", ForumPostViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='forumpost-detail'),
    path("",include("users.urls")),
]
