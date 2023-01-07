from typing import List, Type
from abc import ABC
import json

from channels.generic.websocket import AsyncWebsocketConsumer

from twitter.permissions import  BasePermissionAsync

T = List[Type[BasePermissionAsync]]

class BaseConsumer(AsyncWebsocketConsumer, ABC):
    PermissionClasses: T

    def get_permission_classes(self) -> T:
        return self.PermissionClasses

    async def check_permission(self) -> None:
        for permission in self.get_permission_classes():
            if not permission.has_permission(self):
                message = self.scope.get('error', None) or json.dumps({
                    "message": 'permission denied'
                })
                await self.close(code=4003)