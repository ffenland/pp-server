from django.urls import path
from . import views

urlpatterns = [
    path("", views.ResumeView.as_view()),
    path("<str:pk>/", views.ResumeDetailView.as_view()),
    path("<str:pk>/record/", views.ResumeRecord.as_view()),
]
