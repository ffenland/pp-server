from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.utils.crypto import get_random_string
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_202_ACCEPTED
from .utils import getSidoList, getSggList, convert_code_to_str
import requests


class SidoListView(APIView):
    def get(self, request):
        sido_list = getSidoList()
        if sido_list != None:
            return Response(sido_list, status=HTTP_200_OK)
        else:
            return Response(None, status=HTTP_400_BAD_REQUEST)


class SggListView(APIView):
    def get(self, request, sido):
        sgg_list = getSggList(sido)
        return Response(sgg_list, status=HTTP_200_OK)


class ConvertCodeToStr(APIView):
    def get(self, request, code):
        address = convert_code_to_str(code)
        return Response(address, status=HTTP_200_OK)
