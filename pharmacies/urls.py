from django.urls import path
from .views import PharmacyAccountView

urlpatterns = [
    path("account/", PharmacyAccountView.as_view()),
]
