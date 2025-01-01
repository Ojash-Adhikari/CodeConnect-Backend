from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils.timezone import now
from .choices import UserTypeChoices
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser,PermissionsMixin):
    user_type = models.CharField(
        max_length=20,
        choices=UserTypeChoices.choices,
        default=UserTypeChoices.USER,
        )
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(unique=True)
    

    @property
    def profile(self):
        # Check user type and return the correct related object
        if self.user_type == UserTypeChoices.ADMIN:
            return getattr(self, 'admin', None)
        elif self.user_type == UserTypeChoices.USER:
            return getattr(self, 'user', None)
        return None
