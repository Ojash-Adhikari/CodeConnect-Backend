from django.test import TestCase

from ..models import CustomUser, UserProfile
from .factories import CustomUserFactory, UserProfileFactory


class UserProfileTestCase(TestCase):
    def test_create_user_profile(self):
        """Test that UserProfile can be created using its factory."""

        obj = UserProfileFactory()
        assert UserProfile.objects.all().get() == obj


class CustomUserTestCase(TestCase):
    def test_create_custom_user(self):
        """Test that CustomUser can be created using its factory."""

        obj = CustomUserFactory()
        assert CustomUser.objects.all().get() == obj
