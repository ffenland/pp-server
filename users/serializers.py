from rest_framework.serializers import ModelSerializer
from .models import User
from pharmacies.serializers import PharmacySerializer


class TinyUserSerializer(ModelSerializer):
    """For CafeDetail"""

    class Meta:
        model = User
        fields = (
            "username",
            "avatar",
        )


class MeUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "is_approved",
            "is_complete",
            "is_owner",
            "id",
            "email",
            "username",
            "avatar",
        )


class PrivateUserSerializer(ModelSerializer):
    pharmacy = PharmacySerializer()

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
            "is_complete",
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
            "id",
            "avatar",
            "is_owner",
            "email",
        )
