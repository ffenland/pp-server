from django.urls import path
from .views import (
    NaverLogin,
    KakaoLogin,
)

urlpatterns = [
    path("naver/", NaverLogin.as_view()),
    path("kakao/", KakaoLogin.as_view()),
]
