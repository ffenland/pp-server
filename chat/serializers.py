from rest_framework.serializers import ModelSerializer
from .models import ChatRoom, ChatMessage


class ChatRommSerializer(ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = "__all__"


class ChatMessageSerializer(ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = (
            "created_at",
            "message_body",
            "sender",
        )
