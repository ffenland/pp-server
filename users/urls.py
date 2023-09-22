from django.urls import path
from .views import (
    NaverLogin,
    KakaoLogin,
    Me,
    LogOut,
    PublicUser,
    TestLogin,
    Profile,
    UserAddress,
    UserResume,
)

urlpatterns = [
    path("me/", Me.as_view()),
    path("naver/", NaverLogin.as_view()),
    path("kakao/", KakaoLogin.as_view()),
    path("log-out/", LogOut.as_view()),
    path("test-login/", TestLogin.as_view()),
    path("profile/", Profile.as_view()),
    path("profile/address/", UserAddress.as_view()),
    path("resume/", UserResume.as_view()),
    path("@<str:id>/", PublicUser.as_view()),
]
