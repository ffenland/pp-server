from rest_framework.serializers import ModelSerializer, SerializerMethodField
from users.serializers import TinyUserSerializer
from medias.serializers import PhotoSerializer
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


class PostCreateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class PostSerializer(ModelSerializer):
    user = TinyUserSerializer(read_only=True)
    photo_set = PhotoSerializer(
        read_only=True,
        many=True,
    )
    like_count = SerializerMethodField()
    bad_count = SerializerMethodField()
    fav_count = SerializerMethodField()

    def get_like_count(self, post):
        return post.postrecord_set.filter(kind="like").count()

    def get_bad_count(self, post):
        return post.postrecord_set.filter(kind="bad").count()

    def get_fav_count(self, post):
        return post.postrecord_set.filter(kind="fav").count()

    class Meta:
        model = Post
        fields = "__all__"


class ReplySerializer(ModelSerializer):
    user = TinyUserSerializer()
    is_me = SerializerMethodField()

    def get_is_me(self, reply):
        request = self.context.get("request")
        return request.user == reply.user

    class Meta:
        model = Reply
        fields = ("user", "article", "created_at", "reply", "id", "is_me")
