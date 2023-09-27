from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.utils.crypto import get_random_string
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_202_ACCEPTED,
    HTTP_201_CREATED,
)

from .serializers import MeUserSerializer, PublicUserSerializer, PrivateUserSerializer
from .models import User
from schedules.models import Resume
from medias.models import Photo
from pharmacies.models import Pharmacy
import requests


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


def set_reg_image(cf_id, uploader, pharmacy):
    Photo.objects.create(
        cf_id=cf_id,
        uploader=uploader,
        description="Registration Image",
        pharmacy=pharmacy.id,
    )


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = MeUserSerializer(user)
        return Response(serializer.data)


class Signup(APIView):
    def post(self, request):
        print(request.data)
        request.data = {
            "user": {
                "username": "ㅁㅇㄴ",
                "licenseNum": "11111",
                "sidoCode": "11",
                "sggCode": "650",
                "addressStr": "서울특별시 서초구",
            },
            "pharmacy": {
                "title": "ABC약국",
                "regNum": "3333333333",
                "addressDetail": "1",
                "sidoCode": "11",
                "sggCode": "650",
                "strAddress": "서울 서초구 강남대로 27",
                "ok": True,
            },
        }
        # first save user profile
        user = request.user
        # front에서 받아온 정보 가공하기
        raw_user_data = request.data.get("user")
        user_data = {
            "username": raw_user_data["username"],
            "license_number": raw_user_data["licenseNum"],
            "phone": raw_user_data["phone"] if "phone" in raw_user_data else None,
            "address_sido_code": raw_user_data["sidoCode"],
            "address_sgg_code": raw_user_data["sggCode"],
            "address_str": raw_user_data["addressStr"],
        }
        if raw_user_data["licenseImgId"]:
            # make relation of Photo model to User model
            set_license_image(raw_user_data["licenseImgId"], request.user)

        raw_pharm_data = request.data.get("pharmacy")
        if raw_pharm_data:
            user_data["is_owner"] = True
        serializer = PrivateUserSerializer(
            user,
            data=user_data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            if raw_pharm_data:
                pharm_data = {
                    "title": raw_pharm_data["title"],
                    "owner": request.user,
                    "reg_number": raw_pharm_data["regNum"],
                    "address_sido_code": raw_pharm_data["sidoCode"],
                    "address_sgg_code": raw_pharm_data["sggCode"],
                    "address_str": raw_pharm_data["strAddress"],
                    "address_detail": raw_pharm_data["addressDetail"],
                }
                pharmacy = Pharmacy.objects.create(data=pharm_data)
                if raw_pharm_data["regImgId"]:
                    set_reg_image(
                        cf_id=raw_pharm_data["regImgId"],
                        uploader=request.user,
                        phamacy=pharmacy,
                    )

            else:
                return Response({"ok": True}, status=HTTP_200_OK)

        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


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
                        username=make_ran_username(),
                        email=email,
                        naver_id=naver_id,
                    )
                    user.set_unusable_password()
                    user.save()
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
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)

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


class UserAddress(APIView):
    def get(self, request):
        """get Current Address Value"""
        user = request.user
        sido_code = user.address_sido_code
        sgg_code = user.address_sgg_code
        address_str = user.address_str

        # 넷중 하나라도 None 이면 false
        if sido_code and sgg_code:
            return Response(
                {
                    "setted": True,
                    "data": {
                        "sidoCode": sido_code,
                        "sggCode": sgg_code,
                        "address_str": address_str,
                    },
                },
                status=HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "setted": False,
                    "data": {
                        "sidoCode": "11",
                        "sggCode": "650",
                        "address_str": "서울특별시 서초구",
                    },
                },
                status=HTTP_200_OK,
            )

    def put(self, request):
        sido = request.data.get("sido")
        sgg = request.data.get("sgg")
        if sido != None and sgg != None:
            # Edit User Info
            user = request.user
            user.address_sido_code = sido.get("code")
            user.address_sido = sido.get("name")
            user.address_sgg_code = sgg.get("code")
            user.address_sgg = sgg.get("name")
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
