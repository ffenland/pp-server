from django.urls import path
from .consumers import ChatConsumer
from .views import ChatRoomListView, ChatMessageListView

websocket_urlpatterns = [
    path("chat/<str:room_name>/", ChatConsumer.as_asgi()),
]

urlpatterns = [
    path("", ChatRoomListView.as_view()),
    path("<str:pk>/messages/", ChatMessageListView.as_view()),
]
