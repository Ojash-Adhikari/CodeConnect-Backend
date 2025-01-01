from rest_framework import routers
from django.urls import include,path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns =[
    path("users/user/",UserViewSet.as_view({'get':'list','post':'create'}),name="users"),
    path("users/user/token/",TokenObtainPairView.as_view(),name="token"),
    path("users/user/token/refresh/",TokenRefreshView.as_view(),name="refresh-token"),
]