from rest_framework.serializers import ModelSerializer
from .models import Day, Schedule, Resume


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

    class Meta:
        model = Resume
        exclude = ("description",)


class HomeScheduleSerializer(ModelSerializer):
    schedule = ScheduleWithDaysSerializer()

    class Meta:
        model = Resume
        fields = (
            "is_recruit",
            "is_regular",
            "schedule",
            "address_sido_code",
            "address_sgg_code",
            "created_at",
        )


class ResumeDetailSerializer(ModelSerializer):
    schedule = ScheduleWithDaysSerializer()

    class Meta:
        model = Resume
        fields = "__all__"
