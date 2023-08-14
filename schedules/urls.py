from django.urls import path
from . import views

urlpatterns = [
    path("", views.ScheduleView.as_view()),
    path("resumes/", views.ResumeView.as_view()),
    path("resumes/<str:pk>/", views.ResumeDetailView.as_view()),
]
