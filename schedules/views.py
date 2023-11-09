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
from uuid import UUID
from .models import Schedule, Day, Resume
from .serializer import (
    DaySerializer,
    ProfileResumeSerializer,
    HomeScheduleSerializer,
    ResumeSerializer,
    ResumeDetailSerializer,
    ResumeLikeCountSerializer,
)
from records.models import ResumeLike


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


class HomeSchedules(APIView):
    serializer_class = HomeScheduleSerializer

    def get(self, request):
        address_sido_code = request.user.address_sido_code
        address_sgg_code = request.user.address_sgg_code
        if not address_sido_code:
            address_sido_code = "11"
        resumes = (
            Resume.objects.filter(
                user__address_sido_code=address_sido_code,
                user__address_sgg_code=address_sgg_code,
                is_recruit=False,
            )
            .exclude(
                user=request.user,
            )
            .order_by("-created_at")[:5]
        )
        resumes_serializer = HomeScheduleSerializer(resumes, many=True)
        recruits = (
            Resume.objects.filter(
                user__address_sido_code=address_sido_code,
                user__address_sgg_code=address_sgg_code,
                is_recruit=True,
            )
            .exclude(
                user=request.user,
            )
            .order_by("-created_at")[:5]
        )
        recruits_serializer = HomeScheduleSerializer(recruits, many=True)
        return Response(
            {
                "ok": True,
                "data": {
                    "resumes": resumes_serializer.data,
                    "recruits": recruits_serializer.data,
                },
            }
        )


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
        sido_code = request.user.address_sido_code
        sgg_code = request.user.address_sgg_code
        address_str = request.user.address_str
        is_recruit = request.user.is_owner
        description = request.data.get("data").get("description")
        working_days = request.data.get("data").get("workingDays")
        schedule = find_or_create_schedule(working_days=working_days)
        if schedule and description and len(description) > 12:
            schedule_id = schedule.id
            user = request.user
            obj, created = Resume.objects.update_or_create(
                user=user,
                schedule_id=schedule_id,
                description=description,
                is_recruit=is_recruit,
                address_sido_code=sido_code,
                address_sgg_code=sgg_code,
                address_str=address_str,
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


class ResumeLikeRecord(APIView):
    def get_object(self, pk):
        try:
            resume = Resume.objects.get(pk=pk)
            return resume
        except Resume.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        resume = self.get_object(pk)
        serializer = ResumeLikeCountSerializer(
            resume,
            context={"request": request},
        )

        return Response(
            {"ok": True, "data": serializer.data},
        )

    def post(self, request, pk):
        resume = self.get_object(pk)
        try:
            record = ResumeLike.objects.get(
                resume=resume,
                user=request.user,
            )
            record.delete()
        except ResumeLike.DoesNotExist:
            # create
            ResumeLike.objects.create(
                resume=resume,
                user=request.user,
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
            serializer = ResumeSerializer(resume)

            return Response({"ok": True, "data": serializer.data})


class UserResume(APIView):
    def get_object(self, user_id):
        try:
            return Resume.objects.get(user_id=user_id)
        except Resume.DoesNotExist:
            return None

    def get(self, request, user_id):
        resume = self.get_object(user_id)
        if resume:
            serializer = HomeScheduleSerializer(resume)
            return Response({"ok": True, "data": serializer.data})
        else:
            return Response(
                {"ok": False, "data": {"erm": "The user doesn't have resume"}}
            )
