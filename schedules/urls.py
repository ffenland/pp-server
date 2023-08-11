from django.urls import path
from . import views

urlpatterns = [
    path("", views.ScheduleView.as_view()),
    path("test", views.TestView.as_view()),
    path("resumes", views.ResumeView.as_view()),
    path("recruit", views.RecruitView.as_view()),
]
