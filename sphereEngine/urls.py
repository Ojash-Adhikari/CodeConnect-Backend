from django.urls import path
from .views import (CompileCodeFormView, CompileCodeView, GetProblemsView,ListCompilersView,GetSubmissionView)

urlpatterns = [
    path('compile/', CompileCodeFormView.as_view(), name='compile_code_form'),
    path('compile/submit/', CompileCodeView.as_view(), name='compile_code'),
    path('get-problems/', GetProblemsView.as_view(), name='get_problems'),
    path('submission1/<int:submission_id>/', GetSubmissionView.as_view(), name='get_submission'),
    path('compilers/', ListCompilersView.as_view(), name='list_compilers'),
]