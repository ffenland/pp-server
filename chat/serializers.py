from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import ChatRoom, ChatMessage


class ChatRommSerializer(ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = "__all__"


class ChatMessageSerializer(ModelSerializer):
    is_me = SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = (
            "created_at",
            "message_body",
            "id",
            "is_me",
        )

    def get_is_me(self, obj):
        # 현재 로그인한 사용자와 sender를 비교하여 True 또는 False 반환
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.sender.id == request.user.id
        return False
