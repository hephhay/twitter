from django.contrib.auth import get_user

from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

from twitter.util import cast_user

class CurrentUserOrAdminOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        user = cast_user(get_user(request))
        if type(obj) == type(user) and obj == user:
            return True
        return request.method in SAFE_METHODS or user.is_staff

class OwnerOrAdminOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if getattr(obj, 'owner_field', None) == request.user.id:
            return True
        return request.method in SAFE_METHODS or request.user.is_staff