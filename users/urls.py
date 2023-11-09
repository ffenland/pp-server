from django.urls import path
from .views import (
    NaverLogin,
    KakaoLogin,
    Me,
    LogOut,
    TestLogin,
    ProfileEdit,
    Profile,
    MyAddress,
    UserResume,
    Signup,
    PublicUser,
    ProfileLikeResumes,
)

urlpatterns = [
    path("me/", Me.as_view()),
    path("naver/", NaverLogin.as_view()),
    path("kakao/", KakaoLogin.as_view()),
    path("log-out/", LogOut.as_view()),
    path("signup/", Signup.as_view()),
    path("test-login/", TestLogin.as_view()),
    path("profile/", Profile.as_view()),
    path("profile/edit/", ProfileEdit.as_view()),
    path("profile/address/", MyAddress.as_view()),
    path("profile/like-resumes/", ProfileLikeResumes.as_view()),
    path("resume/", UserResume.as_view()),
    path("@<str:id>/", PublicUser.as_view()),
]
