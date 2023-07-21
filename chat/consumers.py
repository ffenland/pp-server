import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    print("HI")

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # 채팅 그룹에 입장
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # 채팅 그룹에서 퇴장
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        # 클라이언트로부터 메시지 수신
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # 클라이언트에게 메시지 전송
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    async def chat_message(self, event):
        # 클라이언트로 메시지 전송
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
