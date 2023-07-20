from django.urls import path
from . import views

urlpatterns = [
    path("resumes", views.ResumeList.as_view()),
]
