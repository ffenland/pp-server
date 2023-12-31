from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ParseError, NotFound, ValidationError
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
    HTTP_200_OK,
    HTTP_202_ACCEPTED,
    HTTP_201_CREATED,
)

import random
import requests

from .serializers import (
    MeUserSerializer,
    PublicUserSerializer,
    PrivateUserSerializer,
    SignupUserSerializer,
    MiniProfileSerializer,
    ProfileEditSerializer,
)
from .models import User, UserStatus, MessageToken
from schedules.models import Resume
from schedules.serializer import DaySimpleSerializer
from records.models import ResumeLike
from medias.models import Photo
from common.sms import send_verification


## util
def make_ran_username():
    while True:
        ran_name = f"{get_random_string(length=6)}_N"
        if not User.objects.filter(username=ran_name).exists():
            return ran_name


def set_license_image(cf_id, uploader):
    Photo.objects.create(
        cf_id=cf_id,
        uploader=uploader,
        description="License Image",
    )


def set_user_profile(user, profile):
    if profile.get("licenseImgId"):
        set_license_image(profile.get("licenseImgId"), user)
    data = {
        "nickname": profile.get("nickname"),
        "phone": profile.get("phone"),
        "avatar": profile.get("avatarImgId"),
        "license_number": profile.get("licenseNum"),
        "address_sido_code": profile.get("sidoCode"),
        "address_sgg_code": profile.get("sggCode"),
        "address_str": profile.get("addressStr"),
    }
    serializer = SignupUserSerializer(
        user,
        data=data,
    )
    try:
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user.is_complete = True
        user.save()
        return {"ok": True, "data": serializer.data}
    except ValidationError as e:
        error_messages = {}
        for field, errors in e.detail.items():
            if field == "nickname":
                error_messages["nickname"] = "이미 해당 닉네임은 사용중입니다."
            if field == "phone":
                error_messages["phone"] = "유효하지 않거나 이미 등록된 번호입니다."
            if field == "license_number":
                error_messages["license_number"] = "이미 등록된 면허번호입니다."

        return {"ok": False, "data": error_messages}


def edit_user_profile(user, data):
    user_status = UserStatus.objects.get(user=user)
    data_to_modify = {}
    # username, phone, avatar
    if data.get("username") and user_status.username_modify_limit != 0:
        # modify!!
        data_to_modify["username"] = data.get("username")
        pass
    if data.get("phone"):
        # modify!!
        data_to_modify["phone"] = data.get("phone")
        pass
    if data.get("avatar"):
        # modify!!
        data_to_modify["avatar"] = data.get("avatar")
        pass
    pass


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = MeUserSerializer(user)
        return Response(serializer.data)


class Signup(APIView):
    def post(self, request):
        # user sent signup data

        # first set userprofile
        user_profile = set_user_profile(request.user, request.data.get("user"))

        if not user_profile.get("ok"):
            # 유저에게 뭐가 문제인지 자세히 설명해주자.
            return Response(
                {"ok": False, "data": user_profile.get("data")},
                status=HTTP_400_BAD_REQUEST,
            )
        # user porfile saved.

        # is_complete True
        return Response(
            {"ok": True, "data": {"user": user_profile.get("data")["nickname"]}}
        )


class NaverLogin(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            url = f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={settings.NAVER_CLIENT_ID}&client_secret={settings.NAVER_CLIENT_SECRET}&redirect_uri={settings.NAVER_REDIRECT_URI}&code={code}&state={settings.NAVER_STATE}"
            token_request = requests.post(
                url,
                headers={
                    "Accept": "applications/json",
                    "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
                    "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
                },
            )
            access_token = token_request.json().get("access_token")
            result_data = requests.get(
                "https://openapi.naver.com/v1/nid/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "applications/json",
                },
            )
            user_data = result_data.json()

            if user_data.get("resultcode") == "00":
                email = user_data.get("response").get("email")
                naver_id = user_data.get("response").get("id")
                try:
                    user = User.objects.get(email=email)
                    login(request, user)
                except User.DoesNotExist:
                    # signup
                    user = User.objects.create(
                        username=f"nvr{naver_id}",
                        nickname=f"nvr{naver_id}",
                        email=email,
                        naver_id=naver_id,
                    )
                    user.set_unusable_password()
                    user.save()
                    # create user status
                    UserStatus.objects.create(user=user)
                    login(request, user)
                return Response(status=HTTP_200_OK)
            else:
                return Response(status=HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=HTTP_400_BAD_REQUEST)


class KakaoLogin(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            url = "https://kauth.kakao.com/oauth/token"
            token_request = requests.post(
                url,
                data={
                    "grant_type": "authorization_code",
                    "client_id": settings.KAKAO_CLIENT_ID,
                    "client_secret": settings.KAKAO_CLIENT_SECRET,
                    "redirect_uri": settings.KAKAO_REDIRECT_URI,
                    "code": code,
                },
                headers={
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )

            access_token = token_request.json().get("access_token")
            result_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "applications/json",
                },
            )
            user_data = result_data.json()
            if (
                user_data.get("kakao_account").get("email")
                and user_data.get("kakao_account").get("is_email_verified") == True
            ):
                # email 값이 존재하고, email이 verified된 경우
                email = user_data.get("kakao_account").get("email")
                kakao_id = user_data.get("id")
                try:
                    user = User.objects.get(email=email)
                    login(request, user)
                except User.DoesNotExist:
                    # signup
                    user = User.objects.create(
                        username=make_ran_username(),
                        email=email,
                        kakao_id=kakao_id,
                    )
                    user.set_unusable_password()
                    user.save()
                    # create user status
                    UserStatus.objects.create(user=user)
                    login(request, user)
                return Response(status=HTTP_200_OK)
            else:
                return Response(
                    status=HTTP_400_BAD_REQUEST,
                    data={"err": "email not exist or not verified."},
                )
        except Exception:
            return Response(status=HTTP_400_BAD_REQUEST)


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "Bye Bye"})


class PublicUser(APIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            raise NotFound
        serializer = PublicUserSerializer(user)
        return Response(serializer.data)


class TestLogin(APIView):
    def get(self, request):
        users = User.objects.order_by("username")[:10]
        user_data = [{"id": user.id, "username": user.username} for user in users]
        return Response({"ok": True, "data": user_data})

    def post(self, request):
        try:
            user = User.objects.get(pk=request.data.get("id"))
        except User.DoesNotExist:
            raise NotFound

        login(request, user)
        return Response(status=HTTP_200_OK)


class Profile(APIView):
    """Profile page"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user:
            return Response(status=HTTP_400_BAD_REQUEST)
        serializer = PrivateUserSerializer(user)
        return Response({"ok": True, "data": serializer.data})

    def put(self, request):
        # just get username, phone, avatar,
        # address
        user = request.user
        data = request.data
        serializer = PrivateUserSerializer(
            instance=user,
            data=data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"ok": True, "data": serializer.data}, status=HTTP_202_ACCEPTED
            )
        else:
            return Response(
                {"ok": False, "error": serializer.errors}, status=HTTP_400_BAD_REQUEST
            )


class ProfileEdit(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user:
            return Response({"ok": False, "data": {"erm": "User not exists"}})
        serializer = ProfileEditSerializer(user)
        return Response({"ok": True, "data": serializer.data})

    def put(self, request):
        return Response({"ok": True})


class MyAddress(APIView):
    def get(self, request):
        """get Current Address Value"""
        user = request.user
        sido_code = user.address_sido_code
        sgg_code = user.address_sgg_code
        address_str = user.address_str

        # 셋중 하나라도 None 이면 false
        if sido_code and sgg_code and address_str:
            return Response(
                {
                    "ok": True,
                    "data": {
                        "sidoCode": sido_code,
                        "sggCode": sgg_code,
                        "addressStr": address_str,
                    },
                },
                status=HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "ok": False,
                    "data": None,
                },
                status=HTTP_204_NO_CONTENT,
            )

    def put(self, request):
        sido = request.data.get("sido")
        sgg = request.data.get("sgg")
        if sido != None and sgg != None:
            # Edit User Info
            user = request.user
            user.address_sido_code = sido.get("code")
            user.address_sgg_code = sgg.get("code")
            user.address_str = f"{sido.get('name')} {sgg.get('name')}"
            user.save()
            return Response({"ok": True}, status=HTTP_202_ACCEPTED)
        else:
            return Response({"ok": False}, status=HTTP_400_BAD_REQUEST)


class UserResume(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        resume = Resume.objects.filter(user=request.user).first()
        if resume == None:
            return Response({"ok": False})
        else:
            return Response({"ok": True, "resume": resume.id})


class ProfileLikeResumes(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        resume_likes = ResumeLike.objects.filter(user=request.user)
        resume_info_list = []
        for resume_like in resume_likes:
            days_list = []
            if resume_like.resume != None:
                for day in resume_like.resume.schedule.days.all():
                    days_list.append(
                        {
                            "date": day.date,
                            "am": day.am,
                            "pm": day.pm,
                        }
                    )

                resume_info = {
                    "id": resume_like.resume.id,
                    "days": days_list,
                    "nickname": resume_like.resume.user.nickname,
                    "isRecruit": resume_like.resume.is_recruit,
                    "isActive": resume_like.resume.is_active,
                }
                resume_info_list.append(resume_info)

        return Response({"ok": True, "data": {"resumes": resume_info_list}})


class Token(APIView):
    def get(self, request):
        phone = request.query_params.get("phone")
        if not phone:
            return Response(
                {"ok": False, "data": {"ems": "폰 번호가 올바르지 않습니다."}},
                status=HTTP_400_BAD_REQUEST,
            )

        try:
            existing_token = MessageToken.objects.filter(
                user=request.user, phone_number=phone
            ).first()
            if existing_token and existing_token.expires_at > timezone.now():
                # 만료 시간이 양수인 경우 (아직 유효한 토큰이 있는 경우)
                delta = existing_token.expires_at - timezone.now()
                return Response(
                    {
                        "ok": False,
                        "data": {
                            "ems": f"이미 생성된 토큰이 있습니다. {delta.seconds // 60}분 {delta.seconds % 60}초 후에 다시 시도하세요."
                        },
                    },
                    status=HTTP_400_BAD_REQUEST,
                )

            verification_code = str(random.randint(100000, 999999))
            token = MessageToken.objects.create(
                user=request.user,
                phone_number=phone,
                verification_code=verification_code,
            )
            result = send_verification(phone, token.verification_code)
            if not result:
                return Response({"ok": False, "data": {"ems": "인증문자 발신에 실패했습니다."}})
            return Response(
                {
                    "ok": True,
                }
            )

        except Exception as e:
            return Response({"ok": False, "data": {"ems": "알 수 없는 오류가 발생했습니다."}})

    def post(self, request):
        # 사용자로 부터 토큰값을 받은 경우.
        # 토큰값 일치 = 토큰삭제 및 phone 정보 등록
        verification_code = request.data.get("verificationCode")
        phone_number = request.data.get("phoneNumber")
        print(verification_code)
        print(phone_number)
        try:
            token = MessageToken.objects.get(
                phone_number=phone_number, user=request.user
            )
            if token.verification_code == verification_code:
                user = User.objects.get(id=request.user.id)
                user.phone = phone_number
                user.save()
                return Response({"ok": True})
            else:
                return Response({"ok": False})
        except MessageToken.DoesNotExist:
            return Response({"ok": False})
