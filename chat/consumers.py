from channels.db import database_sync_to_async
import json
from .models import ChatMessage, ChatRoom
from channels.generic.websocket import AsyncWebsocketConsumer
from uuid import UUID


class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def save_chat_message(self, chat_room_id, message, sender_id):
        chat_room = ChatRoom.objects.get(id=chat_room_id)
        sender_uuid = UUID(sender_id)
        if (chat_room.first_user.id) != sender_uuid:
            receiver_id = chat_room.first_user.id
        else:
            receiver_id = chat_room.second_user.id

        chat_message = ChatMessage.objects.create(
            chat_room_id=chat_room_id,
            message_body=message,
            sender_id=sender_uuid,
            receiver_id=receiver_id,
        )
        return chat_message

    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["chatroom_id"]
        self.room_group_name = f"chat_{self.room_id}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender_id = text_data_json["sender_id"]
        # Save message to ChatMessage model
        await self.save_chat_message(self.room_id, message, sender_id)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat.message", "message": message, "sender_id": sender_id},
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        sender_id = event["sender_id"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps({"message": message, "sender_id": sender_id})
        )
