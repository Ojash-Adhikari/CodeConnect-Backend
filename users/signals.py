# from django.core.mail import send_mail
# from django.dispatch import receiver
# from django.db.models.signals import pre_save
# from django.db.models.signals import m2m_changed
# from django.utils.timezone import now
# from .models import User

# @receiver(m2m_changed, sender=User)
# def send_otp_email(sender, instance, **kwargs):
#     if instance.pk is None or instance.otp is None:  # New user or no OTP yet
#         instance.generate_otp()  # Generate OTP before saving
#         subject = "Your Verification Code"
#         message = f"Your OTP is {instance.otp}. It will expire in 10 minutes."
#         from_email = "code.connectxhelper@gmail.com"
#         recipient_list = [instance.email]

#         send_mail(subject, message, from_email, recipient_list, fail_silently=False)

from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.timezone import now
import base64
from .models import User

def get_base64_image(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

@receiver(post_save, sender=User)
def send_otp_email(sender, instance, **kwargs):
    if instance.pk is None or instance.otp is None:  # New user or no OTP yet
        instance.generate_otp()  # Generate OTP before saving

        # Email details
        subject = "Your Verification Code"
        from_email = "code.connectxhelper@gmail.com"
        recipient_list = [instance.email]

        logo_base64 = get_base64_image("media/preview-email/logo.svg")


        # Render HTML content from a template
        html_content = render_to_string('email_template.html', {
            'otp': instance.otp,
            'user': instance,
            'logo_base64': logo_base64
        })

        # Strip HTML tags for the plain text version
        text_content = strip_tags(html_content)

        # Create the email object
        email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
        email.attach_alternative(html_content, "text/html")  # Attach HTML content

        # Attach images or GIFs (if needed)
        email.attach_file('media/preview-email/logo.svg', 'image/svg+xml')

        # Send the email
        email.send(fail_silently=False)