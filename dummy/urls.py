from django.urls import path
from . import views

urlpatterns = [
    path("user", views.DummyUser.as_view()),
    path("chat-message", views.DummyChatMessage.as_view()),
    path("account", views.DummyAccount.as_view()),
]
