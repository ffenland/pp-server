from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostListView.as_view()),
    path("<str:pk>/", views.PostDetailView.as_view()),
    path("<str:pk>/reply", views.ReplyView.as_view()),
]
