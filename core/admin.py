from django.contrib import admin

from .models import (CustomUser, UserProfile,Certification,Course,
ForumPost,Exam,Enrollment,Lesson,UserComplaint, Activity)


class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser


class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    
class CertificationAdmin(admin.ModelAdmin):
    model = Certification


class CourseAdmin(admin.ModelAdmin):
    model = Course

class LessonAdmin(admin.ModelAdmin):
    model=Lesson

class EnrollmentAdmin(admin.ModelAdmin):
    model = Enrollment

class UserComplaintAdmin(admin.ModelAdmin):
    model = UserComplaint

class ExamAdmin(admin.ModelAdmin):
    model = Exam


class ForumPostAdmin(admin.ModelAdmin):
    model = ForumPost

class ActivityAdmin(admin.ModelAdmin):
    model = Activity

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Certification, CertificationAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson,LessonAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(UserComplaint,UserComplaintAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(ForumPost, ForumPostAdmin)
admin.site.register(Activity, ActivityAdmin)

