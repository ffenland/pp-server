from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError
from .models import User
from pharmacies.serializers import PharmacySerializer
from schedules.serializer import ProfileResumeSerializer


class TinyUserSerializer(ModelSerializer):
    """For CafeDetail"""

    class Meta:
        model = User
        fields = (
            "username",
            "avatar",
        )


class MiniProfileSerializer(ModelSerializer):
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
            "address_sido_code",
            "address_sgg_code",
        )


class PrivateUserSerializer(ModelSerializer):
    pharmacy = PharmacySerializer()
    resume = ProfileResumeSerializer(source="resume_set", many=True, read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        is_naver = bool(data.get("naver_id"))
        is_kakao = bool(data.get("kakao_id"))

        data.update({"naver_id": is_naver, "kakao_id": is_kakao})
        return data

    class Meta:
        model = User
        exclude = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "license_number",
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
            "nickname",
            "id",
            "avatar",
            "is_owner",
            "email",
        )


class SignupUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "nickname",
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
                "nickname",
                "license_number",
                "address_sido_code",
                "address_sgg_code",
                "address_str",
            ]
            for field in required_fields:
                if data.get(field) is None:
                    raise ValidationError({field: [f"{field} field is required."]})

            return data


class ProfileEditSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "nickname",
            "phone",
            "avatar",
        )
