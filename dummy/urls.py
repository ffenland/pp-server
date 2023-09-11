from django.urls import path
from . import views

urlpatterns = [
    path("user", views.DummyUser.as_view()),
    path("chat-message", views.DummyChatMessage.as_view()),
    path("account", views.DummyAccount.as_view()),
    path("post", views.DummyPost.as_view()),
    path("reply", views.DummyReply.as_view()),
    path("bs4", views.DummyBSparse.as_view()),
]
