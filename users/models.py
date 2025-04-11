from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils.timezone import now
from .choices import UserTypeChoices
from phonenumber_field.modelfields import PhoneNumberField
import random
import datetime

class User(AbstractUser,PermissionsMixin):
    user_type = models.CharField(
        max_length=20,
        choices=UserTypeChoices.choices,
        default=UserTypeChoices.USER,
        )
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(unique=True)
    country = models.ForeignKey('cities_light.Country', on_delete=models.SET_NULL, null=True, blank=True)
    
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))  # 6-digit OTP
        self.otp_expiry = datetime.datetime.now() + datetime.timedelta(minutes=10)  # OTP valid for 10 minutes
        self.save()

    @property
    def profile(self):
        # Check user type and return the correct related object
        if self.user_type == UserTypeChoices.ADMIN:
            return getattr(self, 'admin', None)
        elif self.user_type == UserTypeChoices.USER:
            return getattr(self, 'user', None)
        return None
 