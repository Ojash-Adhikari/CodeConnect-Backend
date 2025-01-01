from django.db import models
from django.conf import settings
from django.core.validators import (MaxLengthValidator,MinLengthValidator,RegexValidator,)
from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
import random
import string
from .choices import UserCompaintChoices

class BaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def all_objects(self):
        return super().get_queryset()

    def deleted(self):
        return super().get_queryset().filter(is_deleted=True)

    def get_all_objects(self):
        return super().get_queryset()

    def get_deleted_objects(self):
        return super().get_queryset().filter(is_deleted=True)

    def get_object(self, pk):
        return super().get_queryset().get(pk=pk)

    def get_object_or_none(self, pk):
        try:
            return super().get_queryset().get(pk=pk)
        except self.model.DoesNotExist:
            return None


class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="created_%(app_label)s_%(class)s",
        null=True,
        blank=True,
        )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="updated_%(app_label)s_%(class)s",
        null=True,
        blank=True,
        )
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="deleted_%(app_label)s_%(class)s",
        null=True,
        blank=True,
        )

    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = BaseManager()

    class Meta:
        abstract = True

    @property
    def permanent_delete(self):
        return False

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.permanent_delete:
            return self.hard_delete(*args, **kwargs)

        return self.soft_delete(*args, **kwargs)

    def undelete(self, *args, **kwargs):
        self.deleted_at = None
        self.is_deleted = False
        super().save(*args, **kwargs)

    def soft_delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.is_deleted = True
        super().save(*args, **kwargs)

    def hard_delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

class UserProfile(BaseModel):
    user = models.OneToOneField(
        "users.User",
        related_name="user_profile",
        on_delete=models.CASCADE,
    )
    banner = models.ImageField(
        upload_to="userprofile/banner/",
        max_length=255,
        help_text="User's profile banner image",
    )
    profile_picture = models.ImageField(
        upload_to="userprofile/profile_picture/",
        max_length=255,
        help_text="User's profile picture",
    )
    description = models.TextField (
        max_length=255,
        help_text="Users decription which can be entered by the user"
    )


class CustomUser(BaseModel):
    user = models.OneToOneField(
        "users.User",
        related_name="custom_user",
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=255,
        help_text="User's name",
    )
    email = models.EmailField(
        max_length=255,
        help_text="User's email address",
    )
    username = models.CharField(
        max_length=150,
        help_text="User's username",
    )
    password = models.CharField(
        max_length=128,
        help_text="User's password",
    )

class Course(BaseModel):
    name = models.CharField(
        max_length=100,
        help_text="The name of the course",
    )
    description = models.TextField(
        help_text="Description of the course",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the course was created",
    )
    updated_at = models.DateTimeField(
        help_text="Date and time when the course was last updated",
    )
    courseId = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
        null=True,
        blank=True,
        help_text="Unique ID for the course",
    )
    duration = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    def save(self, *args, **kwargs):
        if not self.courseId:
            self.courseId = self.generate_unique_id()
        super().save(*args, **kwargs)

    def generate_unique_id(self):
        length = 10
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

class Lesson(BaseModel):
    course = models.ForeignKey(
        "core.Course",
        related_name="lessons",
        on_delete=models.CASCADE,
        help_text="The course the user is enrolled in",
    )
    name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="The name of the lesson",
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Description of the lesson",
    )
    picture = models.ImageField(
        upload_to="course/lesson/lessonpicture/",
        max_length=255,
        null=True,
        help_text="Lesson picture entered by admin",
    )
    duration = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

class Enrollment(BaseModel):
    user = models.ForeignKey(
        "users.User",
        related_name="enrollments",
        on_delete=models.CASCADE,
        help_text="The user enrolled in the course",
    )
    course = models.ForeignKey(
        "core.Course",
        related_name="enrollments",
        on_delete=models.CASCADE,
        help_text="The course the user is enrolled in",
    )
    enrolled_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the user enrolled in the course",
    )


class Exam(BaseModel):
    course = models.ForeignKey(
        "core.Course",
        related_name="exams",
        on_delete=models.CASCADE,
        help_text="The course related to the exam",
    )
    user = models.ForeignKey(
        "users.User",
        related_name="exams",
        on_delete=models.CASCADE,
        help_text="The user taking the exam",
    )
    passed = models.BooleanField(
        help_text="Indicates if the user passed the exam",
    )


class Certification(BaseModel):
    user = models.ForeignKey(
        "users.User",
        related_name="certifications",
        on_delete=models.CASCADE,
        help_text="The user who received the certification",
    )
    course = models.ForeignKey(
        "core.Course",
        related_name="certifications",
        on_delete=models.CASCADE,
        help_text="The course for which the certification is provided",
    )
    issued_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the certification was issued",
    )

class UserComplaint(BaseModel):
    user = models.ForeignKey(
        "users.User",
        related_name="user_complaint",
        on_delete=models.CASCADE,
        help_text="The user who have submitted complaints",
    )
    subject = models.TextField(
        max_length=100
    )
    related = models.CharField(
        max_length=50,
        choices=UserCompaintChoices.choices,
        default=UserCompaintChoices.WEBSITE,
    )
    complain = models.TextField(
        max_length=255,
    )

class Review(BaseModel):
    user = models.ForeignKey(
        "users.User",
        related_name="user_review",
        on_delete=models.CASCADE,
        help_text="The user who have submitted review",
    )
    course = models.ForeignKey(
        "core.Course",
        related_name="reviews",
        on_delete=models.CASCADE,
        help_text="The course the user reviewed",
    )
    description = models.TextField(
        max_length=255,
    )

class ForumPost(BaseModel):
    user = models.ForeignKey(
        "users.User",
        related_name="forum_posts",
        on_delete=models.CASCADE,
        help_text="The user who created the forum post",
    )
    title = models.CharField(
        max_length=200,
        help_text="Title of the forum post",
    )
    content = models.TextField(
        help_text="Content of the forum post",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the post was created",
    )

class Admin(BaseModel):
    name= models.CharField(max_length=255,)
    email = models.EmailField(null=False,unique=True)
    def __str__(self):
        """String representation of an Admin instance."""
        return self.name

class User(BaseModel):
    name= models.CharField(max_length=255,)
    email = models.EmailField(null=False,unique=True)
    def __str__(self):
        """String representation of an User instance."""
        return self.name