from rest_framework import routers
from django.urls import include,path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, send_otp, verify_otp, preview_email
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns =[
    path("users/user/",UserViewSet.as_view({'get':'list','post':'create'}),name="users"),
    path('users/user/<int:pk>/update/', UserViewSet.as_view({'patch': 'update_user'}), name='update-user'),
    path("users/user/token/",TokenObtainPairView.as_view(),name="token"),
    path("users/user/token/refresh/",TokenRefreshView.as_view(),name="refresh-token"),
    path("send-otp/", send_otp, name="send-otp"),
    path("verify-otp/", verify_otp, name="verify-otp"),
    path('preview-email/', preview_email, name='preview_email'),

]