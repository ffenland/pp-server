from django.urls import path
from .views import (
    Me,
    Users,
    PublicUser,
    NaverLogin,
    KakaoLogin,
)

urlpatterns = [
    path("", Users.as_view()),
    path("me/", Me.as_view()),
    path("naver/", NaverLogin.as_view()),
    path("kakao/", KakaoLogin.as_view()),
    path("@<str:username>/", PublicUser.as_view()),
]
