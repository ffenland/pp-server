import traceback

from django.db.models import Count, Q
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
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
    ProfileResumeSerializer,
    HomeScheduleSerializer,
    ResumeSerializer,
    ResumeDetailSerializer,
)
from records.models import Record


def str_to_bool(value):
    return value.lower() == "true"


def find_or_create_schedule(working_days):
    """1차로 Days를 찾고 2차로 Days를 가진 Schedule을 찾는다."""
    day_ids = []  # 일자별 Day 모델의 ID를 저장할 리스트

    # workingDays를 순회하면서 해당하는 Day 모델을 찾거나 생성
    for day, values in working_days.items():
        try:
            # 해당하는 Day 모델을 찾음
            day_obj = Day.objects.get(date=day, am=values["am"], pm=values["pm"])
            day_ids.append(day_obj.id)  # Day 모델의 ID를 저장
        except Day.DoesNotExist:
            # 해당하는 Day 모델이 없으면 생성
            day_obj = Day(date=day, am=values["am"], pm=values["pm"])
            day_obj.save()
            day_ids.append(day_obj.id)  # 새로 생성한 Day 모델의 ID를 저장

    # Day_ids를 이용해 스케줄을 찾거나 만든다.

    if len(day_ids) != 0:
        day_count = len(day_ids)
        day_list = Day.objects.filter(id__in=day_ids)

        schedule = Schedule.objects.annotate(day_count=Count("days")).filter(
            day_count=day_count
        )
        for day in day_list:
            schedule = schedule.filter(days=day)
        schedule = schedule.first()
        if schedule == None:
            schedule = Schedule.objects.create()
            schedule.days.add(*day_list)
            return schedule
        else:
            return schedule


class HomeSchedules(generics.ListAPIView):
    serializer_class = HomeScheduleSerializer

    def get_queryset(self):
        address_sido_code = self.request.user.address_sido_code
        if not address_sido_code:
            address_sido_code = "11"
        queryset = Resume.objects.filter(
            user__address_sido_code=address_sido_code,
        ).order_by("-created_at")[:5]

        return queryset


# Create your views here.


class ResumeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sido_code = request.user.address_sido_code
        sgg_code = request.user.address_sgg_code

        one_week_ago = timezone.now() - timedelta(days=7)

        recruits = Resume.objects.filter(
            ~Q(user=request.user),
            is_recruit=True,
            user__address_sido_code=sido_code,
            user__address_sgg_code=sgg_code,
            # created_at__gte=one_week_ago,
        ).order_by("-created_at")[:5]
        resumes = Resume.objects.filter(
            ~Q(user=request.user),
            is_recruit=False,
            user__address_sido_code=sido_code,
            user__address_sgg_code=sgg_code,
            # created_at__gte=one_week_ago,
        ).order_by("-created_at")[:5]
        resume_serializer = ResumeSerializer(resumes, many=True)
        recruit_serializer = ResumeSerializer(recruits, many=True)
        return Response(
            {
                "ok": True,
                "resumes": resume_serializer.data,
                "recruits": recruit_serializer.data,
            }
        )

    def post(self, request):
        """Create or Update Resume"""

        is_recruit = request.user.is_owner
        description = request.data.get("data").get("description")
        working_days = request.data.get("data").get("workingDays")
        schedule = find_or_create_schedule(working_days=working_days)
        if schedule and description and len(description) > 10:
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
                {"ok": True, "id": serializer.data.get("id")}, status=HTTP_201_CREATED
            )
        else:
            traceback.print_exc()  # Print traceback
            raise ParseError


class ResumeEdit(APIView):
    def put(self, request):
        try:
            is_recruit = request.user.is_owner
            description = request.data.get("data").get("description")
            working_days = request.data.get("data").get("workingDays")
            address = request.data.get("data").get("address")
            resume_id = request.data.get("data").get("resumeId")
            schedule = find_or_create_schedule(working_days=working_days)

            if schedule and description and len(description) > 10:
                user = request.user
                resume = Resume.objects.get(id=resume_id)
                resume.schedule = schedule
                data = {
                    "description": description,
                    "is_recruit": is_recruit,
                    "user": user.id,
                    "address_sido_code": address.get("sidoCode"),
                    "address_sgg_code": address.get("sggCode"),
                }
                serializer = ResumeDetailSerializer(
                    resume,
                    data=data,
                    partial=True,
                )
                if serializer.is_valid():
                    serializer.save()  # Save the serializer data

                    return Response(
                        {"ok": True, "id": serializer.data.get("id")},
                        status=HTTP_201_CREATED,
                    )
                else:
                    print(serializer.errors)
                    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
            else:
                raise ParseError("Invalid data")
        except Exception as e:
            traceback.print_exc()  # Print traceback for debugging
            raise ParseError(str(e))


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


class CountResume(APIView):
    def get(self, request):
        # return current User's resume count
        # til now limit is one
        try:
            user = request.user
            resume_count = Resume.objects.filter(user=user).count()
            return Response({"ok": True, "count": resume_count})

        except Exception as e:
            print(e)
            raise ParseError


class MyResume(APIView):
    def get_object(self, user):
        return Resume.objects.filter(user=user).first()

    def get(self, request):
        resume = self.get_object(request.user)
        if not resume:
            return Response(
                {
                    "ok": False,
                }
            )
        else:
            serializer = ProfileResumeSerializer(resume)
            return Response({"ok": True, "data": serializer.data})
