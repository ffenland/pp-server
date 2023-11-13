from common.utils import convert_code_to_str
from rest_framework.serializers import (
    ModelSerializer,
    ReadOnlyField,
    SerializerMethodField,
)

from .models import Day, Schedule, Resume


class DaySerializer(ModelSerializer):
    def get_unique_together_validators(self):
        """Overriding method to disable unique together checks"""
        return []

    class Meta:
        model = Day
        fields = "__all__"


class DaySimpleSerializer(ModelSerializer):
    class Meta:
        model = Day
        fields = ("date",)


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
    is_regular = ReadOnlyField()

    class Meta:
        model = Resume
        exclude = ("updated_at",)


class HomeScheduleSerializer(ModelSerializer):
    schedule = ScheduleWithDaysSerializer()
    like_count = SerializerMethodField()

    class Meta:
        model = Resume
        fields = (
            "id",
            "is_recruit",
            "is_regular",
            "schedule",
            "like_count",
            "created_at",
        )

    def get_like_count(self, resume):
        return resume.resumelike_set.count()


class ProfileResumeSerializer(ModelSerializer):
    schedule = ScheduleWithDaysSerializer()

    class Meta:
        model = Resume
        fields = (
            "schedule",
            "id",
            "is_recruit",
            "is_regular",
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


class ResumeLikeCountSerializer(ModelSerializer):
    like = SerializerMethodField()
    was_i = SerializerMethodField()

    def get_like(self, obj):
        return obj.resumelike_set.count()

    def get_was_i(self, obj):
        current_user = self.context["request"].user
        return obj.resumelike_set.filter(user=current_user).exists()

    class Meta:
        model = Resume
        fields = (
            "like",
            "was_i",
        )
