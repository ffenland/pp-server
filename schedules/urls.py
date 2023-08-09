from django.urls import path
from . import views

urlpatterns = [
    path("", views.ScheduleView.as_view()),
    path("test", views.TestView.as_view()),
    path("resumes", views.ResumeList.as_view()),
]
