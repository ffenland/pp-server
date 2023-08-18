from django.db.models import Q
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.pagination import CursorPagination
from .models import ChatRoom, ChatMessage
from .serializers import ChatRommSerializer, ChatMessageSerializer


class ChatRoomListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_objects(self, user):
        try:
            return ChatRoom.objects.filter(Q(first_user=user) | Q(second_user=user))
        except ChatRoom.DoesNotExist:
            raise NotFound

    def get(self, request):
        chat_rooms = self.get_objects(request.user)
        response_data = []
        for chat in chat_rooms:
            partner = (
                chat.second_user if chat.first_user == request.user else chat.first_user
            )
            latest_message = chat.messages.order_by("-created_at").first()
            response_data.append(
                {
                    "partner": {
                        "username": partner.username,
                        "avatar": partner.avatar,
                    },
                    "last_message": {
                        "message": latest_message.message_body[:40] + "..."
                        if latest_message
                        else "",
                        "created_at": latest_message.created_at
                        if latest_message
                        else "",
                    },
                    "chatroom_id": chat.pk,
                }
            )

        return Response({"ok": True, "data": response_data})


class CustomCursorPagination(CursorPagination):
    page_size = 20  # 한 페이지에 보여질 메시지 개수
    ordering = "-created_at"  # 메시지 생성일 기준으로 정렬


class ChatMessageListView(generics.ListAPIView):
    serializer_class = ChatMessageSerializer
    pagination_class = CustomCursorPagination

    def get_queryset(self):
        chat_room_id = self.kwargs.get("pk")
        queryset = ChatMessage.objects.filter(chat_room_id=chat_room_id).order_by(
            "-created_at"
        )
        return queryset
