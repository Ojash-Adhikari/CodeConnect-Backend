from django.urls import path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

TITLE = "User registration and profile customization"
DESCRIPTION = """
A login and registration system where users have to input their name, age, email, username and password to registered then can use email and password to login. The user should also be able to customize their profile with banners, profile pictures, edit their name, email and password. The user can also delete their profile if they wish so.
"""
VERSION = "1.0.0"


urlpatterns = [
    path(
        "schema/",
        get_schema_view(title=TITLE, description=DESCRIPTION, version=VERSION),
        name="openapi-schema",
    ),
    path(
        "swagger-ui/",
        TemplateView.as_view(
            template_name="openapi/swagger-ui.html",
            extra_context={"schema_url": "openapi-schema"},
        ),
        name="swagger-ui",
    ),
]
