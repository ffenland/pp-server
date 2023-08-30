from django.urls import path
from .views import PharmacyAccountView, PharmacyAccountOneDayView

urlpatterns = [
    path("account/", PharmacyAccountView.as_view()),
    path("account/<str:date>/", PharmacyAccountOneDayView.as_view()),
]
