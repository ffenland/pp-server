from faker import Faker
from chat.models import ChatRoom, ChatMessage
from django.contrib.auth.models import User
from django.utils import timezone
import random

fake = Faker()

chat_room = ChatRoom.objects.get(pk="c5878c75-c088-42fa-876a-3f8077a75aea")

# ChatMessage 생성
chat_messages = []
for _ in range(100):  # 각각의 ChatRoom에 100개의 ChatMessage 생성
    sender = chat_room.first_user if _ % 2 == 0 else chat_room.second_user
    receiver = (
        chat_room.second_user
        if sender == chat_room.first_user
        else chat_room.first_user
    )
    chat_messages.append(
        ChatMessage(
            chat_room=chat_room,
            message_body=fake.text(),
            sender=sender,
            receiver=receiver,
            created_at=timezone.now(),
        )
    )

ChatMessage.objects.bulk_create(chat_messages)  # 한 번에 생성
