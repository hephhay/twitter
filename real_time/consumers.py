import json
from typing import Union

from channels.db import database_sync_to_async

from twitter.consumers import BaseConsumer
from twitter.permissions import IsAuthenticated
from real_time.models import Clients


class ChatConsumer(BaseConsumer):
    PermissionClasses = [IsAuthenticated]

    async def receive(self, text_data: Union[str, bytes, bytearray]):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.send(text_data=json.dumps({"message": message}))


class NotificatonConsumer(BaseConsumer):
    PermissionClasses = [IsAuthenticated]

    @database_sync_to_async
    def initialize(self) -> None:
        Clients.objects.create(user=self.scope['user'], channel_name=self.channel_name)
        print(self.scope['user'])
        print(self.channel_name)

    async def receive(self, text_data: Union[str, bytes, bytearray]):
        # print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.send(text_data=json.dumps({"message": message}))

    @database_sync_to_async
    def destroy(self) -> None:
        Clients.objects.get(channel_name=self.channel_name).delete()

    # Receive message chahnnel layer
    async def notify_user(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))