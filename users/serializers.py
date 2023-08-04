from rest_framework.serializers import ModelSerializer
from .models import User


class TinyUserSerializer(ModelSerializer):
    """For CafeDetail"""

    class Meta:
        model = User
        fields = (
            "username",
            "avatar",
        )


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "id",
            "password",
            "first_name",
            "last_name",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
            "last_login",
            "groups",
            "user_permissions",
        )


class PublicUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "avatar",
            "isHost",
            "gender",
            "language",
            "currency",
        )
