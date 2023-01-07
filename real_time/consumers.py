import json
from typing import Union

from twitter.consumers import BaseConsumer
from twitter.permissions import IsAuthenticated


class ChatConsumer(BaseConsumer):
    PermissionClasses = [IsAuthenticated]

    async def connect(self):
        await self.check_permission()
        await self.accept()

    async def receive(self, text_data: Union[str, bytes, bytearray]):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        message = text_data_json['message']
        await self.send(text_data=json.dumps({"message": message}))
