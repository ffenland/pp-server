from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver
from common.models import CommonPKModel, CommonModel

# Create your models here.


class ChatRoom(CommonPKModel, CommonModel):
    first_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_query_name="chat_member_one",
        related_name="chat_member_one",
    )
    second_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_query_name="chat_member_two",
        related_name="chat_member_two",
    )

    def __str__(self):
        return f"{self.first_user.username} & {self.second_user.username} Chat"


class ChatMessage(CommonPKModel, CommonModel):
    chat_room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_query_name="messages",
        related_name="messages",
    )
    message_body = models.TextField()
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_query_name="msg_sender",
        related_name="msg_sender",
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_query_name="msg_receiver",
        related_name="msg_receiver",
    )

    def __str__(self):
        return f"{self.message_body[:10]} by {self.sender.username} to {self.receiver.username}"


@receiver(pre_save, sender=ChatRoom)
def validate_unique_user_pair(sender, instance, **kwargs):
    if instance.first_user_id is not None and instance.second_user_id is not None:
        if instance.first_user_id >= instance.second_user_id:
            raise ValidationError("Invalid user pair for ChatRoom")


@receiver(pre_save, sender=ChatMessage)
def validate_valid_sender_and_receiver(sender, instance, **kwargs):
    if (
        instance.sender_id == instance.chat_room.first_user_id
        and instance.receiver_id == instance.chat_room.second_user_id
    ) or (
        instance.sender_id == instance.chat_room.second_user_id
        and instance.receiver_id == instance.chat_room.first_user_id
    ):
        pass  # Valid sender and receiver
    else:
        raise ValidationError("Invalid sender and receiver for ChatMessage")
