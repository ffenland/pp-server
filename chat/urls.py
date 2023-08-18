from django.urls import path

from .views import ChatRoomListView, ChatMessageListView


urlpatterns = [
    path("", ChatRoomListView.as_view()),
    path("<str:pk>/messages/", ChatMessageListView.as_view()),
]
