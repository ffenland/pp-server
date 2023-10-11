from django.urls import path
from . import views

urlpatterns = [
    path("", views.ResumeView.as_view()),
    path("my/", views.MyResume.as_view()),
    path("edit/", views.ResumeEdit.as_view()),
    path("home/", views.HomeSchedules.as_view()),
    path("howmany/", views.CountResume.as_view()),
    path("<str:pk>/", views.ResumeDetailView.as_view()),
    path("<str:pk>/record/", views.ResumeRecord.as_view()),
]
