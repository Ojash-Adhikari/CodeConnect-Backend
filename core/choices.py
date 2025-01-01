from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class UserCompaintChoices(TextChoices):
    COURSES = "COURSES", _("Courses")
    QUESTIONS = "QUESTIONS", _("Questions")
    CODE_EDITOR = "CODE_EDITOR", _("Code_editor")
    WEBSITE = "WEBSITE", _("Website")

