from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class UserTypeChoices(TextChoices):
    ADMIN = "ADMIN", _("Admin")
    USER = "USER", _("User")

