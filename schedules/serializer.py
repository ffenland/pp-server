from rest_framework.serializers import ModelSerializer
from .models import Day, Schedule


class DaySerializer(ModelSerializer):
    def get_unique_together_validators(self):
        """Overriding method to disable unique together checks"""
        return []

    class Meta:
        model = Day
        fields = "__all__"


class ScheduleSerializer(ModelSerializer):
    days = DaySerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Schedule
        fields = "__all__"

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     print("Serialized Data:", data)  # 디버깅 출력 추가
    #     return data
