from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.db.models import Q
from django.utils.dateformat import DateFormat

import traceback
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
from collections import defaultdict
from .models import Pharmacy, Account
from .serializers import PharmacyAccountSerializer


def organize_accounts_by_date(accounts):
    organized_data = defaultdict(list)

    for account in accounts:
        year, month, day = account.get_date_info()  # Account 모델에 있는 메서드 활용
        date_str = f"{year}/{month:02}"  # 월을 2자리로 포맷
        organized_data[date_str].append(account)

    return organized_data


class PharmacyAccountView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, user):
        try:
            pharmacy = Pharmacy.objects.get(owner=user)
            return pharmacy
        except Pharmacy.DoesNotExist:
            raise NotFound

    def get(self, request):
        current_date = make_aware(datetime.now())
        pharmacy = self.get_object(request.user)
        date_range = [current_date - timedelta(days=i) for i in range(7)]
        account_list = []
        for date in date_range:
            account = Account.objects.filter(pharmacy=pharmacy, date=date)
            if len(account) == 0:
                continue
            else:
                serializer = PharmacyAccountSerializer(
                    account,
                    many=True,
                )
                account_list.append(
                    {"date": date.strftime("%Y-%m-%d"), "accounts": serializer.data}
                )

        return Response({"ok": True, "pharmacy": pharmacy.id, "accounts": account_list})

    def post(self, request):
        # create one days account
        if not request.user:
            return Response({"ok": False}, status=400)
        pharmacy = self.get_object(request.user)
        date = request.data.get("date")
        try:
            accounts = request.data.get("accounts")
            for key, value in accounts.items():
                if len(value) != 0:
                    obj, created = Account.objects.update_or_create(
                        name=key,
                        date=date,
                        pharmacy=pharmacy,
                    )
                    obj.ammount = value
                    obj.save()
            return Response({"ok": True})
        except Exception:
            traceback.print_exc()  # Print traceback
            raise ParseError("An error occurred")


class PharmacyAccountOneDayView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, user):
        try:
            pharmacy = Pharmacy.objects.get(owner=user)
            return pharmacy
        except Pharmacy.DoesNotExist:
            raise NotFound

    def get(self, request, date):
        if not date:
            return Response({"ok": False, "error": "Not valid date"})
        pharmacy = self.get_object(request.user)
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        accounts = Account.objects.filter(pharmacy=pharmacy, date=date_obj)
        account_obj = {}
        for account in accounts:
            key = account.name
            value = account.ammount
            if key and value:
                account_obj[key] = value

        return Response({"ok": True, "data": account_obj}, status=HTTP_200_OK)


class PharmacyAccountMonthView(APIView):
    def get_object(self, user):
        try:
            pharmacy = Pharmacy.objects.get(owner=user)
            return pharmacy
        except Pharmacy.DoesNotExist:
            raise NotFound

    def get(self, request, date):
        # date = 6digit YYYYMM]
        if len(date) == 6:
            pharmacy = self.get_object(request.user)
            year = int(date[:4])
            month = int(date[4:])
            # 월의 앞의 0 삭제
            formatted_month = str(month).lstrip("0")
            date_filter = Q(
                date__year=year, date__month=formatted_month, pharmacy=pharmacy
            )
            filtered_accounts = Account.objects.filter(date_filter)
            organized_accounts = organize_accounts_by_date(filtered_accounts)
            for date, accounts in organized_accounts.items():
                print(f"{date}: {len(accounts)} 거래 기록")
                for account in accounts:
                    print(f" - {account}")
            return Response({"ok": True})
        else:
            return Response({"ok": False}, status=HTTP_400_BAD_REQUEST)
