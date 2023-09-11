from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from users.models import User
from chat.models import ChatMessage, ChatRoom
from pharmacies.models import Pharmacy, Account
from posts.models import Post, Reply
import faker
import random
import string
import traceback
import requests
from datetime import datetime, timedelta
from django.utils import timezone
from bs4 import BeautifulSoup
from common.utils import getSidoList, getSggList


class DummyUser(APIView):
    def post(self, request):
        """create dummy users"""
        fake = faker.Faker("ko_KR")

        def generate_random_string(length):
            digits = string.digits  # 숫자 문자열 '0123456789'
            return "".join(random.choice(digits) for _ in range(length))

        def create_dummy_users(num_users=50):
            for _ in range(num_users):
                User.objects.create(
                    username=fake.user_name(),
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    email=fake.email(),
                    phone=generate_random_string(11),
                    naver_id=generate_random_string(5),
                    kakao_id=generate_random_string(5),
                    avatar=fake.image_url(),
                    license_number=fake.random_int(min=100000, max=999999),
                    license_img=fake.image_url(),
                    college=fake.word(),
                    year_of_admission=fake.random_int(min=1900, max=2150),
                    address_sgg_code=fake.random_int(min=10000, max=99999),
                    address_sido=fake.city(),
                    address_sgg=fake.city_suffix(),
                )

        try:
            create_dummy_users()
            return Response(status=200)
        except:
            traceback.print_exc()  # Print traceback
            raise ParseError


class DummyChatMessage(APIView):
    def post(self, request):
        try:
            fake = faker.Faker()
            chatrooms = ChatRoom.objects.all()
            for chat_room in chatrooms:
                chat_messages = []
                for _ in range(100):
                    sender = (
                        chat_room.first_user if _ % 2 == 0 else chat_room.second_user
                    )
                    receiver = (
                        chat_room.second_user
                        if sender == chat_room.first_user
                        else chat_room.first_user
                    )
                    # 랜덤한 시간 범위 설정 (예: 현재 시간에서 0~3600초 사이)
                    time_offset = random.randint(0, 3600)
                    created_at = timezone.now() - timezone.timedelta(
                        seconds=time_offset
                    )
                    chat_messages.append(
                        ChatMessage(
                            chat_room=chat_room,
                            message_body=fake.text(),
                            sender=sender,
                            receiver=receiver,
                            created_at=created_at,
                        )
                    )
                ChatMessage.objects.bulk_create(chat_messages)
            return Response(status=200)
        except Exception as e:
            print("An error occurred:", e)
            traceback.print_exc()  # Print traceback
            raise ParseError("An error occurred")


class DummyAccount(APIView):
    def get_object(self, user):
        try:
            pharmacy = Pharmacy.objects.get(owner=user)
            return pharmacy
        except Pharmacy.DoesNotExist:
            raise NotFound

    def post(self, request):
        try:
            current_date = datetime.now().date()
            one_yeaer_ago = current_date - timedelta(days=365)
            pharmacy = self.get_object(request.user)

            for choice in Account.AccountNames.choices:
                temp_date = current_date
                name = choice[0]

                while temp_date >= one_yeaer_ago:
                    ammount = random.randint(3000, 20000) * 100
                    does_existing_account = Account.objects.filter(
                        date=temp_date,
                        name=name,
                        pharmacy=pharmacy,
                    ).exists()
                    if not does_existing_account:
                        account = Account.objects.create(
                            name=name,
                            date=temp_date,
                            pharmacy=pharmacy,
                            ammount=ammount,
                        )
                    temp_date -= timedelta(days=1)

            return Response(status=200)
        except Exception as e:
            print("An error occurred:", e)
            traceback.print_exc()  # Print traceback
            raise ParseError("An error occurred")


class DummyPost(APIView):
    def post(self, request):
        """Create Dummpy Post"""

        def generate_random_string(length):
            digits = string.digits  # 숫자 문자열 '0123456789'
            return "".join(random.choice(digits) for _ in range(length))

        def create_dummy_post(num_posts=50):
            fake = faker.Faker("ko_KR")
            for _ in range(num_posts):
                random_user = User.objects.order_by("?").first()
                if random_user is not None:
                    choices = [choice[0] for choice in Post.PostKindChoices.choices]
                    random_choice = random.choice(choices)
                    Post.objects.create(
                        user=random_user,
                        title=fake.sentence()[:29],
                        article=fake.text(),
                        kind=random_choice,
                    )

        try:
            create_dummy_post()
            return Response(status=200)
        except:
            traceback.print_exc()  # Print traceback
            raise ParseError


class DummyReply(APIView):
    def post(self, request):
        """Create Dummy Reply"""
        pass


class DummyBSparse(APIView):
    def post(self, request):
        sido_list = getSidoList()
        if sido_list:
            print("Sido List:", sido_list)
        sido_code = "51"
        sgg_list = getSggList(sido_code)
        print(sgg_list)
        return Response({"ok": True}, status=200)
