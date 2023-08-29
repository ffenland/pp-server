from datetime import datetime, timedelta
from django.utils.timezone import make_aware
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

from .models import Pharmacy, Account
from .serializers import PharmacyAccountSerializer


class PharmacyAccountView(APIView):
    def get_object(self, user):
        try:
            pharmacy = Pharmacy.objects.get(owner=user)
            return pharmacy
        except Pharmacy.DoesNotExist:
            raise NotFound

    def get(self, request):
        current_date = make_aware(datetime.now())
        eight_days_ago = current_date - timedelta(days=8)
        pharmacy = self.get_object(request.user)
        recent_seven = Account.objects.filter(
            pharmacy=pharmacy,
            date__gte=eight_days_ago,
            date__lte=current_date,
        )
        serializer = PharmacyAccountSerializer(
            recent_seven,
            many=True,
        )
        return Response(
            {"ok": True, "pharmacy": pharmacy.id, "accounts": serializer.data}
        )


class PharmacyCalculateView(APIView):
    pass
