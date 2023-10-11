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
    ValidationError,
)
from rest_framework.pagination import CursorPagination
from collections import defaultdict
from .models import Pharmacy, Account
from .serializers import PharmacyAccountSerializer, PharmacySerializer
from medias.models import Photo


def organize_accounts_by_date(accounts):
    """return {"yyyy-mm-dd":{"cash":foo-bar,"income":foo-bar, "card":foo-bar, "prepare":foo-bar},}"""
    organized_data = defaultdict(dict)

    for account in accounts:
        year, month, day = account.get_date_info()  # Account 모델에 있는 메서드 활용
        date_str = f"{year}-{month:02}-{day:02}"  # 월,일을 2자리로 포맷

        organized_data[date_str][account.name] = account.ammount

    return dict(sorted(organized_data.items(), reverse=False))


def set_reg_image(cf_id, uploader, pharmacy):
    Photo.objects.create(
        cf_id=cf_id,
        uploader=uploader,
        description="Registration Image",
        pharmacy=pharmacy,
    )


def set_pharmacy_profile(user, pharmacy):
    user.is_owner = True
    user.save()
    data = {
        "title": pharmacy.get("title"),
        "owner": user.id,
        "reg_number": pharmacy.get("regNum"),
        "address_str": pharmacy.get("strAddress"),
        "address_detail": pharmacy.get("addressDetail"),
        "address_sido_code": pharmacy.get("sidoCode"),
        "address_sgg_code": pharmacy.get("sggCode"),
    }
    serializer = PharmacySerializer(data=data)
    try:
        serializer.is_valid(raise_exception=True)
        if pharmacy.get("regImageId"):
            set_reg_image(pharmacy.get("regImageId"), user, serializer.instance)
        serializer.save()
        user.is_owner_complete = True
        user.save()
        return {"ok": True, "data": serializer.data}
    except ValidationError as e:
        return {"ok": False, "data": e.detail}


class PharmacyCreate(APIView):
    def post(self, request):
        pharmacy_data = request.data
        pharmacy_profile = set_pharmacy_profile(request.user, pharmacy_data)
        if not pharmacy_profile.get("ok"):
            return Response(
                {"ok": False, "data": pharmacy_profile.get("data")},
                status=HTTP_400_BAD_REQUEST,
            )
        else:
            return Response(
                {"ok": True, "data": pharmacy_profile.get("data")}, status=HTTP_200_OK
            )


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


class PharmacyAccountDateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, user):
        try:
            pharmacy = Pharmacy.objects.get(owner=user)
            return pharmacy
        except Pharmacy.DoesNotExist:
            raise NotFound

    def get(self, request, date):
        # date formant YYYY-MM-DD
        print("DATE", date)
        pharmacy = self.get_object(request.user)
        try:
            if len(date) == 10:
                # Day
                date_obj = datetime.strptime(date, "%Y-%m-%d").date()
                print("DATE_OBJ", date_obj)
                accounts = Account.objects.filter(pharmacy=pharmacy, date=date_obj)
                print("ACCOUNTS", accounts)
                account_obj = {}
                account_obj[date] = defaultdict(dict)
                # account가 아예 없는 경우가 있구나...
                for account in accounts:
                    key = account.name
                    value = account.ammount
                    account_obj[date][key] = value if value is not None else 0
                return Response({"ok": True, "data": account_obj}, status=HTTP_200_OK)
            elif len(date) == 7:
                # Month
                date_obj = datetime.strptime(date, "%Y-%m").date()
                date_filter = Q(
                    date__year=date_obj.year,
                    date__month=date_obj.month,
                    pharmacy=pharmacy,
                )
                filtered_accounts = Account.objects.filter(date_filter)

                organized_accounts = organize_accounts_by_date(filtered_accounts)
                return Response({"ok": True, "data": organized_accounts})
            else:
                return Response(
                    {"ok": False, "error": "Not valid date"},
                    status=HTTP_400_BAD_REQUEST,
                )
        except Exception:
            traceback.print_exc()  # Print traceback
            return Response(
                {"ok": False, "error": "Not valid date or ProcessError"},
                status=HTTP_400_BAD_REQUEST,
            )
