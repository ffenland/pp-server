from django.db import transaction
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from .models import Schedule

# Create your views here.


class ResumeList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        region_code = request.user.address_sgg_code
        if not region_code or len(region_code) != 5:
            region_code = "11680"  # seoul gangnam-gu

        return Response({"ok": True, "region_code": region_code})
