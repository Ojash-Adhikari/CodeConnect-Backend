from django.utils.timezone import now
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import User
from users.serializers import UserSerializer, VerifyOTPSerializer, SendOTPSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.core.mail import send_mail

from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from users.permissions import IsOwnUser
from cities_light.models import Country


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_permissions(self):
        # Allow anyone to create a new user (register), but require authentication for all other actions.
        if self.action in ['create']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated,IsOwnUser,]
        return super().get_permissions()
    
    @action(detail=True, methods=['patch'])
    def update_user(self, request, pk=None):
        user = self.get_object()
        if user != request.user:
            return Response({"detail": "You can only update your own data."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def register(self, request, *args, **kwargs):
        """
        Custom register action that uses the same serializer.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)
    
@api_view(["POST","GET"])
def send_otp(request):
    serializer = SendOTPSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data["username"]
        user = User.objects.get(username=username)
        
        user.generate_otp()
        
        send_mail(
            "Your Verification Code",
            f"Your OTP is {user.otp}. It will expire in 10 minutes.",
            "code.connectxhelper@gmail.com",
            [user.email],
        )
        return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST","GET"])
def verify_otp(request):
    serializer = VerifyOTPSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data["username"]
        otp = serializer.validated_data["otp"]
        user = User.objects.get(username=username)

        user.is_active = True  # Activate account
        user.otp = None  # Clear OTP
        user.otp_expiry = None
        user.save()

        return Response({"message": "Account activated successfully"}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Email Templates Test
def preview_email(request):
    context = {
        'otp': '123456',  
        'user': {
            'username': 'JohnDoe',  
        },
    }

    # Render the HTML email template
    html_content = render_to_string('email_template.html', context)

    # Return the rendered HTML as a response
    return HttpResponse(html_content)