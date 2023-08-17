from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.utils.crypto import get_random_string
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

from .serializers import MeUserSerializer, PublicUserSerializer
from .models import User
import requests


## util
def make_ran_username():
    while True:
        ran_name = f"{get_random_string(length=6)}_N"
        if not User.objects.filter(username=ran_name).exists():
            return ran_name


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = MeUserSerializer(user)
        return Response(serializer.data)


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

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        serializer = PublicUserSerializer(user)
        return Response(serializer.data)


class TestLogin(APIView):
    def post(self, request):
        try:
            user = User.objects.get(username="ffenland")
        except User.DoesNotExist:
            raise NotFound
        print(user)
        login(request, user)
        return Response(status=HTTP_200_OK)
