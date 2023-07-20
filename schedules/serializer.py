from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Day, Schedule


class DaySerializer(ModelSerializer):
    class Meta:
        model = Day
        fields = (
            "date",
            "am",
            "pm",
        )


class SmallScheduleSerializer(ModelSerializer):
    day_set = DaySerializer(
        many=True,
    )

    class Meta:
        model = Schedule
        fields = "__all__"
