from __future__ import annotations
from typing import TYPE_CHECKING

from django.contrib.auth import get_user
from django.utils.decorators import classonlymethod
from abc import abstractmethod, ABC

from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

from utils.helpers import cast_user

class CurrentUserOrAdminOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        user = cast_user(get_user(request))
        if type(obj) == type(user) and obj == user:
            return True
        return request.method in SAFE_METHODS or user.is_staff

class OwnerOrAdminOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):

        if getattr(obj, view.owner_field, None) == request.user:
            return True
        return request.method in SAFE_METHODS or request.user.is_staff


if TYPE_CHECKING:
    from twitter.consumers import BaseConsumer


class BasePermissionAsync(ABC):

    @classonlymethod
    @abstractmethod
    def has_permission(cls, consumer: BaseConsumer) -> bool:
        pass

class IsAuthenticated(BasePermissionAsync):

    @classonlymethod
    def has_permission(cls, consumer: BaseConsumer) -> bool:
        return consumer.scope['user'].is_authenticated
