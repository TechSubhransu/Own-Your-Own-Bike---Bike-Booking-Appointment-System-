import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'support_chat'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        print("✅ WebSocket connected:", self.scope["user"])

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print("❌ WebSocket disconnected")

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user = self.scope["user"]
        username = user.username if user.is_authenticated else "Guest"
        print("📩 Message received from:", user, "→", message)

        if user.is_authenticated:
            await self.save_message(user, message)

        # broadcast to all connected clients (admin + users)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username']
        }))
        print("📤 Message broadcasted:", event['username'], "→", event['message'])

    @database_sync_to_async
    def save_message(self, user, message):
        Message.objects.create(
            user=user,
            content=message,
            is_admin=user.is_staff
        )
