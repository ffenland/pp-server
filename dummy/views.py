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
import faker
import random
import string
import traceback
from django.utils import timezone


class DummyUser(APIView):
    def post(self, request):
        """create dummy users"""
        fake = faker.Faker()

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
                    phone=fake.phone_number(),
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
