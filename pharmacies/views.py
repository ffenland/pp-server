from datetime import datetime

from django.db.models import Q
from django.utils.dateformat import DateFormat

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.pagination import CursorPagination

from .models import Pharmacy
from .serializers import PharmacySerializer


class PharmacyAccountView(APIView):
    def get_object(self, user):
        try:
            pharmacy = Pharmacy.objects.get(owner=user)
            return pharmacy
        except Pharmacy.DoesNotExist:
            raise NotFound

    def get(self, request):
        pharmacy = self.get_object(request.user)
        serializer = PharmacySerializer(pharmacy)
        return Response(serializer.data)


class PharmacyCalculateView(APIView):
    pass
