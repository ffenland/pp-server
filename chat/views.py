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


class ChatView(APIView):
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
                        "nickname": partner.nickname,
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

    def post(self, request):
        first_user = request.data.get("firstUserId")
        second_user = request.data.get("secondUserId")
        if first_user == None or second_user == None:
            return Response(
                {"ok": False, "data": {"erm": "user ID value is worng."}},
                status=HTTP_400_BAD_REQUEST,
            )
        # Ensure that first_user and second_user are in ascending order.
        if first_user > second_user:
            first_user, second_user = second_user, first_user

        chat_room_list = ChatRoom.objects.filter(
            first_user_id=first_user, second_user_id=second_user
        )
        if len(chat_room_list):
            chat_room = chat_room_list.first()

        else:
            try:
                chat_room = ChatRoom.objects.create(
                    first_user_id=first_user, second_user_id=second_user
                )

            except:
                # 사용자를 찾을 수 없을 경우 예외 처리를 수행할 수 있습니다.
                return Response(
                    {"ok": False, "data": {"erm": "wrong user Id"}},
                    status=HTTP_400_BAD_REQUEST,
                )

        return Response({"ok": True, "data": {"chatRoomId": chat_room.id}})


class ChatRoomView(APIView):
    def get_object(self, pk):
        try:
            return ChatRoom.objects.get(pk=pk)
        except ChatRoom.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            chatroom = self.get_object(pk)
            if not request.user.id in [
                chatroom.first_user.id,
                chatroom.second_user.id,
            ]:
                return Response(
                    {
                        "ok": False,
                        "data": {
                            "opponentNickname": "",
                            "opponentAvatar": "",
                            "opponentId": "",
                        },
                    },
                    status=HTTP_400_BAD_REQUEST,
                )
            opponent = (
                chatroom.first_user
                if request.user == chatroom.second_user
                else chatroom.second_user
            )
            return Response(
                {
                    "ok": True,
                    "data": {
                        "opponentNickname": opponent.nickname,
                        "opponentAvatar": opponent.avatar,
                        "opponentId": opponent.id,
                    },
                }
            )
        except:
            return Response(
                {
                    "ok": False,
                    "data": {
                        "opponentNickname": "",
                        "opponentAvatar": "",
                        "opponentId": "",
                    },
                },
                status=HTTP_400_BAD_REQUEST,
            )


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
