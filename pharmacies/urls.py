from django.urls import path
from .views import PharmacyAccountView, PharmacyAccountDateView, PharmacyCreate

urlpatterns = [
    path("create/", PharmacyCreate.as_view()),
    path("account/", PharmacyAccountView.as_view()),
    path("account/<str:date>/", PharmacyAccountDateView.as_view()),
]
