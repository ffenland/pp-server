from django.urls import path
from .views import (
    PharmacyAccountView,
    PharmacyAccountOneDayView,
    PharmacyAccountMonthView,
)

urlpatterns = [
    path("account/", PharmacyAccountView.as_view()),
    path("account/month/<str:date>/", PharmacyAccountMonthView.as_view()),
    path("account/day/<str:date>/", PharmacyAccountOneDayView.as_view()),
]
