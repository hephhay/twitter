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
            'is_verified'
        )

class UserSerializer(UserSerial):

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
        ) +  ('id', 'is_verified', 'created_at', 'updated_at')
        read_only_fields = (settings.LOGIN_FIELD,)