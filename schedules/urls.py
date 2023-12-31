from django.urls import path
from . import views

urlpatterns = [
    path("", views.ResumeView.as_view()),
    path("my/", views.MyResume.as_view()),
    path("edit/", views.ResumeEdit.as_view()),
    path("home/", views.HomeSchedules.as_view()),
    path("howmany/", views.CountResume.as_view()),
    path("user/<str:user_id>/", views.UserResume.as_view()),
    path("<str:pk>/", views.ResumeDetailView.as_view()),
    path("<str:pk>/like/", views.ResumeLikeRecord.as_view()),
]
