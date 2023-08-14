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
    ResumeDetailSerializer,
)
from records.models import Record


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

        return schedule
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
            "is_recruit": "False",
        }

        get_day_ids(request.data)
        return Response(status=HTTP_200_OK)


# Create your views here.


class ResumeView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        recruit_param = request.query_params.get("isRecruit")
        is_recruit = recruit_param and recruit_param.lower() == "true"
        if is_recruit:
            resumes = Resume.objects.filter(is_recruit=True)
        else:
            resumes = Resume.objects.filter(is_recruit=False)
        serializer = ResumeSerializer(resumes, many=True)
        return Response({"ok": True, "resumes": serializer.data})

    def post(self, request):
        """Create or Update Resume"""
        is_recruit = request.data.get("isRecruit")
        description = request.data.get("description")
        days = request.data.get("days")
        schedule = get_schedule(days)
        if description and len(description) > 10 and schedule:
            schedule_id = schedule.id
            user = request.user
            obj, created = Resume.objects.update_or_create(
                user=user,
                schedule_id=schedule_id,
                defaults={"description": description},
                is_recruit=is_recruit,
            )

            serializer = ResumeSerializer(obj)
            return Response(
                {"ok": True, "resume": serializer.data}, status=HTTP_201_CREATED
            )
        else:
            raise ParseError


class ResumeDetailView(APIView):
    def get_object(self, pk):
        try:
            resume = Resume.objects.get(pk=pk)
            return resume
        except Resume.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        resume = self.get_object(pk)
        serializer = ResumeDetailSerializer(resume)
        return Response({"ok": True, "resume": serializer.data})

    def put(self, request, pk):
        description = request.data.get("description")
        days = request.data.get("days")
        resume = self.get_object(pk)
        data = {}

        if description is None and days is None:
            return Response({"ok": False}, status=HTTP_204_NO_CONTENT)
        else:
            if days:
                schedule = get_schedule(days)
                resume.schedule = schedule
            if description:
                data["description"] = description
            serializer = ResumeDetailSerializer(
                resume,
                data=data,
                partial=True,
            )
            if serializer.is_valid():
                serializer.save()
                return Response({"ok": True})
            else:
                return Response({"ok": False, "error": serializer.errors})

    def delete(self, request, pk):
        resume = self.get_object(pk=pk)
        if resume.user == request.user:
            resume.delete()
            return Response({"ok": True}, status=HTTP_204_NO_CONTENT)
        else:
            return Response({"ok": False}, status=HTTP_400_BAD_REQUEST)


class ResumeRecord(APIView):
    def get_object(self, pk):
        try:
            resume = Resume.objects.get(pk=pk)
            return resume
        except Resume.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        kind_param = request.query_params.get("kind")
        kind = kind_param and kind_param.lower()
        resume = self.get_object(pk)
        if kind not in [
            "like",
            "bad",
            "fav",
        ]:
            return Response(
                {"ok": False, "error": "Kind Error"},
                status=HTTP_400_BAD_REQUEST,
            )

        record_count = resume.record_set.filter(kind=kind).count()
        was_i = resume.record_set.filter(kind=kind, user=request.user).exists()

        return Response(
            {"ok": True, "data": {"count": record_count, "wasI": was_i}},
        )

    def post(self, request, pk):
        kind_param = request.query_params.get("kind")
        kind = kind_param and kind_param.lower()
        resume = self.get_object(pk)
        if kind not in [
            "like",
            "bad",
            "fav",
        ]:
            return Response(
                {"ok": False, "error": "Kind Error"},
                status=HTTP_400_BAD_REQUEST,
            )

        try:
            record = Record.objects.get(
                user=request.user,
                kind=kind,
                resume=resume,
            )
            record.delete()
            return Response({"ok": True})
        except Record.DoesNotExist:
            Record.objects.create(
                user=request.user,
                kind=kind,
                resume=resume,
            )
            return Response({"ok": True})
