from rest_framework import serializers
from rest_framework.request import Request
from typing import Union
from drf_writable_nested.serializers import WritableNestedModelSerializer
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.serializers import UserSerializer

from cities_light.models import Country

class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseModel
        fields = (
            "id",
            "is_deleted",
            "created_by",
            "updated_by",
            "deleted_by",
            "created_at",
            "updated_at",
            "deleted_at",
        )
        extra_kwargs = {
            "is_deleted": {"read_only": True},
            "created_by": {"read_only": True},
            "updated_by": {"read_only": True},
            "deleted_by": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "deleted_at": {"read_only": True},
        }

    @property
    def request(self) -> Union[Request, None]:
        return self.context.get("request")

    def save(self, **kwargs):
        manipulation_data = {}
        if self.request:
            if not self.instance:
                manipulation_data["created_by"] = self.request.user
            manipulation_data["updated_by"] = self.request.user
        return super().save(**{**kwargs, **manipulation_data})


class BaseModelWritableNestedModelSerializer(
    WritableNestedModelSerializer, BaseModelSerializer
):
    pass


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = BaseModelSerializer.Meta.fields + ("user", "name", "email", "username", "password")
        extra_kwargs = {"password": {"write_only": True}}


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = BaseModelSerializer.Meta.fields + ("user", "banner", "profile_picture")


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = BaseModelSerializer.Meta.fields + ("user", "course", "issued_at")


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = BaseModelSerializer.Meta.fields + ("name","description","language","courseId","picture","duration","price","is_activated")

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = BaseModelSerializer.Meta.fields + ('course', 'name', 'description', 'picture', 'duration', 'video', 'sections')   

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = BaseModelSerializer.Meta.fields + ("user", "course", "enrolled_at")

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = BaseModelSerializer.Meta.fields + ("title","is_accepted")

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = BaseModelSerializer.Meta.fields + ("title",)

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = BaseModelSerializer.Meta.fields + ("course", "user", "passed")

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = BaseModelSerializer.Meta.fields + ("user", "course", "description","rating")

class ForumPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumPost
        fields = BaseModelSerializer.Meta.fields + ("user", "title", "content", "created_at")

class UserComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserComplaint
        fields = BaseModelSerializer.Meta.fields + ("user","subject","related","complain")

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = BaseModelSerializer.Meta.fields + ("name","email")

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = BaseModelSerializer.Meta.fields + ("name","email")

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name_ascii', 'slug','geoname_id']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user_data = UserSerializer(self.user, context=self.context).data
        
        try:
            profile = self.user.profile
            if isinstance(profile, Admin):
                user_data["profile"] = AdminSerializer(
                    profile, context=self.context
                ).data
            elif isinstance(profile, User):
                user_data["profile"] = UserSerializer(
                    profile, context=self.context
                ).data
        except Admin.DoesNotExist:
            pass
        except User.DoesNotExist:
            pass
        
        data["user"] = user_data
        return data