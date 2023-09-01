from django.urls import path
from .views import PharmacyAccountView, PharmacyAccountDateView

urlpatterns = [
    path("account/", PharmacyAccountView.as_view()),
    path("account/<str:date>/", PharmacyAccountDateView.as_view()),
]
