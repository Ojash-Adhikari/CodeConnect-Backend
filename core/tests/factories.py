from datetime import timezone

import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory

from ..models import CustomUser, UserProfile

User = get_user_model()


class UserProfileFactory(DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = factory.SubFactory("users.tests.factories.UserFactory")


class CustomUserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    user = factory.SubFactory("users.tests.factories.UserFactory")
    name = factory.Faker("bs")
    email = factory.Faker("email")
    username = factory.Faker("bs")
    password = factory.Faker("bs")
