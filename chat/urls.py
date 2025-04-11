from django.urls import path, include
from chat import views as chat_views
from django.contrib.auth.views import LoginView, LogoutView
from .views import generate_question_api
from .views import RandomQuestionAPIView


urlpatterns = [
    path("chat/", chat_views.chatPage, name="chat-page"),
    path('submission/<int:submission_id>/output/', chat_views.submissionOutput, name='fetch_submission_output'),
    #http://127.0.0.1:8000/api/v1/submission/792097978/output/
    # login-section
    path("chat/auth/login/", LoginView.as_view(template_name="chat/LoginPage.html"), name="login-user"),
    path("chat/auth/logout/", LogoutView.as_view(), name="logout-user"),
    path('generate-question/', generate_question_api),
    path('random-question/', RandomQuestionAPIView.as_view(), name='random-question'),
]