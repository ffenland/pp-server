from django.urls import path
from . import views

urlpatterns = [
    path("address/sido/", views.SidoListView.as_view()),
    path("address/sgg/<str:sido>/", views.SggListView.as_view()),
    path("address/convert/<str:code>/", views.ConvertCodeToStr.as_view()),
]
