from rest_framework.serializers import ModelSerializer, SerializerMethodField
from users.serializers import TinyUserSerializer
from .models import Post, Reply


class PostListSerializer(ModelSerializer):
    def get_unique_together_validators(self):
        """Overriding method to disable unique together checks"""
        return []

    user = TinyUserSerializer()

    class Meta:
        model = Post
        fields = ("title", "kind", "user", "created_at", "view_count", "id")


class PostHotSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "kind", "view_count")


class POSTCreateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        post = Post.objects.create(**validated_data)
        return post


class PostSerializer(ModelSerializer):
    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"


class ReplySerializer(ModelSerializer):
    user = TinyUserSerializer()

    class Meta:
        model = Reply
        fields = ("user", "article", "created_at", "reply")
