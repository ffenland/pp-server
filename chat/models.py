from django.db import models
from django.conf import settings
from common.models import CommonPKModel, CommonModel

# Create your models here.


class ChatRoom(CommonPKModel, CommonModel):
    one = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="chat_member_one",
    )
    two = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="chat_member_two",
    )


class ChatMessage(CommonModel):
    text = models.TextField()
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    chat_room = models.ForeignKey(
        ChatRoom, null=True, blank=True, on_delete=models.SET_NULL
    )
