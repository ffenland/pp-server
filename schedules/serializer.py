from rest_framework.serializers import ModelSerializer
from .models import Day, Schedule


class DaySerializer(ModelSerializer):
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
