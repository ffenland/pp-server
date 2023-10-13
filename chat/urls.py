from django.urls import path

from .views import ChatView, ChatRoomView, ChatMessageListView


urlpatterns = [
    path("", ChatView.as_view()),
    path("<str:pk>/", ChatRoomView.as_view()),
    path("<str:pk>/messages/", ChatMessageListView.as_view()),
]
