from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Course, Notification, Activity  # adjust the import based on your app structure

@receiver(post_save, sender=Course)
def create_notification_for_high_price_course(sender, instance, created, **kwargs):
    if created and instance.price and instance.price > 2500 and not (Notification.objects.filter(course=instance).exists()):
        Notification.objects.create(
            course=instance,
            title=f"Course {instance.courseId} added by {instance.created_by.username} exceeds price range, Acceptance is required"
        )

        Activity.objects.create(
            title=f"Course {instance.courseId} was added with a high price by {instance.created_by.username}",
            created_by=instance.created_by
        )
        
@receiver(post_save, sender=Notification)
def activate_course(sender, instance, **kwargs):
    """
    Signal to activate a course when a notification is accepted.
    """
    if instance.is_accepted and not instance.course.is_activated:
        instance.course.is_activated = True
        instance.course.save()

        Activity.objects.create(
            title=f"Course {instance.course.courseId} was activated after notification acceptance",
            created_by=instance.created_by
        )

        instance.delete()

@receiver(post_save, sender=Activity)
def log_activity(sender, instance, created, **kwargs):
    """
    Logs whenever an activity is created.
    """
    if created:
        print(f"Activity Logged: {instance.title} by {instance.created_by}")