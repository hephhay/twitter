from typing import cast

from django.contrib.auth import get_user

from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

from users.models import User

class CurrentUserOrAdminOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        user = cast(User, get_user(request))
        if type(obj) == type(user) and obj == user:
            return True
        return request.method in SAFE_METHODS or user.is_staff