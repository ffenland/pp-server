from django.db import transaction
from django.utils import timezone
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from .models import Schedule, Day, Resume
from .serializer import (
    DaySerializer,
    ScheduleSerializer,
    ResumeSerializer,
)


def str_to_bool(value):
    return value.lower() == "true"


def get_day_ids(data):
    """Day id의 배열을 반환하거나 빈 배열을 반환함."""
    if isinstance(data, list) or isinstance(data, tuple):
        day_ids = []
        for item in data:
            serializer = DaySerializer(data=item)
            if serializer.is_valid():
                date = serializer.validated_data.get("date")
                am = serializer.validated_data.get("am")
                pm = serializer.validated_data.get("pm")
                day, created = Day.objects.get_or_create(date=date, am=am, pm=pm)
                day_ids.append(day.id)
            else:
                return Response(serializer.errors)
        return day_ids
    else:
        return []


def get_schedule(data):
    day_id_list = get_day_ids(data)
    if len(day_id_list) != 0:
        day_count = len(day_id_list)
        day_list = Day.objects.filter(id__in=day_id_list)
        schedule = Schedule.objects.annotate(day_count=Count("days")).filter(
            day_count=day_count
        )
        for day in day_list:
            schedule = schedule.filter(days=day)
        schedule = schedule.first()
        if schedule == None:
            schedule = Schedule.objects.create()
            schedule.days.add(*day_list)
        # Need only SC id.
        serializer = ScheduleSerializer(schedule)
        return serializer.data
    else:
        return None


class TestView(APIView):
    def post(self, request):
        {
            "description": "blabla",
            "days": [
                {"date": "20230809", "am": "False", "pm": "True"},
                {"date": "20230812", "am": "True", "pm": "True"},
                {"date": "20230811", "am": "True", "pm": "True"},
                {"date": "20230813", "am": "True", "pm": "False"},
            ],
        }

        get_day_ids(request.data)
        return Response(status=HTTP_200_OK)


# Create your views here.
class ScheduleView(APIView):
    def post(self, request):
        """receive days list return schedule id"""
        data = request.data
        day_id_list = get_day_ids(data)
        if len(day_id_list) != 0:
            day_count = len(day_id_list)
            day_list = Day.objects.filter(id__in=day_id_list)
            schedule = Schedule.objects.annotate(day_count=Count("days")).filter(
                day_count=day_count
            )
            for day in day_list:
                schedule = schedule.filter(days=day)
            schedule = schedule.first()
            if schedule == None:
                schedule = Schedule.objects.create()
                schedule.days.add(*day_list)
            # Need only SC id.
            serializer = ScheduleSerializer(schedule)
            return Response({"ok": True, "schedule": serializer.data})
        else:
            return Response(
                {
                    "ok": False,
                    "error": "No data provided",
                },
                status=HTTP_400_BAD_REQUEST,
            )


class ResumeView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        recruit_param = request.query_params.get("is_recruit")
        is_recruit = recruit_param and recruit_param.lower() == "true"
        if is_recruit:
            resumes = Resume.objects.filter(is_recruit=True)
        else:
            resumes = Resume.objects.filter(is_recruit=False)
        serializer = ResumeSerializer(resumes, many=True)
        return Response({"ok": True, "resumes": serializer.data})

    def post(self, request):
        is_recruit = request.data.get("isRecruit")
        description = request.data.get("description")
        days = request.data.get("days")
        schedule = get_schedule(days)
        if description and len(description) > 10 and schedule:
            schedule_id = schedule.get("id")
            user = request.user
            obj, created = Recruit.objects.update_or_create(
                user=user,
                schedule_id=schedule_id,
                defaults={"description": description},
                is_recruit=is_recruit,
            )

            serializer = RecruitSerializer(obj)
            return Response({"ok": True, "resume": serializer.data})
        else:
            raise ParseError
