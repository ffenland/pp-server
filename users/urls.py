from django.urls import path
from .views import NaverLogin, KakaoLogin, Me, LogOut, PublicUser, TestLogin

urlpatterns = [
    path("me/", Me.as_view()),
    path("naver/", NaverLogin.as_view()),
    path("kakao/", KakaoLogin.as_view()),
    path("log-out/", LogOut.as_view()),
    path("test-login/", TestLogin.as_view()),
    path("@<str:username>/", PublicUser.as_view()),
]
