from rest_framework.serializers import (
    ModelSerializer,
    ReadOnlyField,
    SerializerMethodField,
)
from .models import Day, Schedule, Resume
from common.utils import convert_code_to_str


class DaySerializer(ModelSerializer):
    def get_unique_together_validators(self):
        """Overriding method to disable unique together checks"""
        return []

    class Meta:
        model = Day
        fields = "__all__"


class ScheduleSerializer(ModelSerializer):
    class Meta:
        model = Schedule
        fields = ("id",)


class ScheduleWithDaysSerializer(ModelSerializer):
    days = DaySerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        model = Schedule
        fields = ("days",)

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     print("Serialized Data:", data)  # 디버깅 출력 추가
    #     return data


class ResumeSerializer(ModelSerializer):
    schedule = ScheduleWithDaysSerializer()
    address_sido_code = ReadOnlyField()
    address_sgg_code = ReadOnlyField()
    address_str = ReadOnlyField()
    is_regular = ReadOnlyField()

    class Meta:
        model = Resume
        exclude = ("description",)


class HomeScheduleSerializer(ModelSerializer):
    schedule = ScheduleWithDaysSerializer()

    class Meta:
        model = Resume
        fields = (
            "id",
            "is_recruit",
            "is_regular",
            "schedule",
            "address_sido_code",
            "address_sgg_code",
            "address_str",
            "created_at",
        )


class ProfileResumeSerializer(ModelSerializer):
    schedule = ScheduleWithDaysSerializer()

    class Meta:
        model = Resume
        fields = (
            "schedule",
            "id",
        )


class ResumeDetailSerializer(ModelSerializer):
    schedule = ScheduleWithDaysSerializer()
    is_regular = ReadOnlyField()
    str_address = SerializerMethodField()

    class Meta:
        model = Resume
        fields = "__all__"

    def get_str_address(self, resume):
        code = resume.address_sido_code + resume.address_sgg_code
        return convert_code_to_str(code)
