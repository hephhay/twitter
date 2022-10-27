from rest_framework import serializers

from django.contrib.auth import get_user_model
from djoser.conf import settings
from djoser.serializers import UserCreateSerializer, UserSerializer as UserSerial

User = get_user_model()

class UserCreate(UserCreateSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            "password",
        )

class UserSerializer(UserSerial):
    num_followers = serializers.IntegerField(read_only = True)

    num_following = serializers.IntegerField(read_only = True)

    follows_you = serializers.BooleanField(read_only = True)

    class Meta:
        model = User
        
        read_only_fields = (
            settings.LOGIN_FIELD,
            'id',
            'created_at',
            'updated_at',
            'is_verified'
        )
        exclude = (
            'password',
            'groups',
            'user_permissions',
            'followers'
        )