from typing import List, Type
from abc import ABC
import json

from channels.generic.websocket import AsyncWebsocketConsumer

from twitter.permissions import  BasePermissionAsync

T = List[Type[BasePermissionAsync]]

class BaseConsumer(AsyncWebsocketConsumer, ABC):
    PermissionClasses: T
    Permitted = False

    def get_permission_classes(self) -> T:
        return self.PermissionClasses

    async def initialize(self) -> bool: ...

    async def connect(self):
        self.permitted = await self.check_permission()
        if self.permitted:
            await self.initialize()
            await self.accept()

    async def check_permission(self) -> bool:
        for permission in self.get_permission_classes():
            if not permission.has_permission(self):
                await self.close(code=4003)
                return False

        return True

    async def destroy(self) -> None: ...

    async def disconnect(self, code) -> None:
        if self.permitted:
            await self.destroy()