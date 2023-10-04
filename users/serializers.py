from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError
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


class SignupUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "phone",
            "license_number",
            "avatar",
            "address_sido_code",
            "address_sgg_code",
            "address_str",
        )

        def validate(self, data):
            # 필수 필드들을 확인하고, 하나라도 None이면 예외 발생
            required_fields = [
                "username",
                "license_number",
                "address_sido_code",
                "address_sgg_code",
                "address_str",
            ]
            for field in required_fields:
                if data.get(field) is None:
                    raise ValidationError({field: [f"{field} field is required."]})

            return data
