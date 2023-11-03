from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostListView.as_view()),
    path("create/", views.PostCreateView.as_view()),
    path("detail/<str:pk>/", views.PostDetailView.as_view()),
    path("detail/<str:pk>/count/", views.PostCountView.as_view()),
    path("detail/<str:pk>/reply/", views.ReplyView.as_view()),
]
