from typing import Any, Optional
from urllib.parse import parse_qs

from django.utils.translation import gettext_lazy as _
from django.db import close_old_connections
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack, UserLazyObject
from channels.db import database_sync_to_async
from rest_framework_simplejwt.authentication import AUTH_HEADER_TYPE_BYTES
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.exceptions import (
    AuthenticationFailed,
    InvalidToken,
    TokenError
)

api_settings: Any = api_settings

AUTH_HEADER_TYPES = api_settings.AUTH_HEADER_TYPES

class JWTMiddleware(BaseMiddleware):
    def __init__(self, inner) -> None:
        self.user_model = get_user_model()
        return super().__init__(inner)

    async def __call__(self, scope, receive, send):
        close_old_connections()
        scope = dict(scope)
        if 'user' not in scope:
            scope['user'] = UserLazyObject()

        try:
            user = await self.authenticate(scope)
            scope['user']._wrapped = user or AnonymousUser()

        except (TokenError, InvalidToken, AuthenticationFailed) as Err:
            scope['error'] = str(Err)
            scope['user']._wrapped = AnonymousUser()

        return await super().__call__(scope, receive, send)

    async def authenticate(self, scope) -> Any:
        query_string = scope['query_string'].decode('utf-8')
        query_params = parse_qs(query_string)

        if  jwt_auth_token := query_params.get('jwt_auth_token', None):
            raw_token = self.get_raw_token(jwt_auth_token[0])

            if raw_token is None:
                return None

            validated_token = self.get_validated_token(raw_token)

            return await self.get_user(validated_token)
        else:
            return None

    def get_validated_token(self, raw_token: str) -> Any:
        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """
        messages = []
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                return AuthToken(raw_token)
            except TokenError as e:
                messages.append({'token_class': AuthToken.__name__,
                                'token_type': AuthToken.token_type,
                                'message': e.args[0]})

        raise InvalidToken({
            'detail': _('Given token not valid for any token type'),
            'messages': messages,
        })

    def get_raw_token(self, header: str) -> Optional[str]:
        """
        Extracts an unvalidated JSON web token from the given "Authorization"
        header value.
        """
        parts = header.split()

        if len(parts) == 0:
            # Empty AUTHORIZATION header sent
            return None

        if parts[0].encode('utf-8') not in AUTH_HEADER_TYPE_BYTES:
            # Assume the header does not contain a JSON web token
            return None

        if len(parts) != 2:
            raise AuthenticationFailed(
                _('Authorization header must contain two space-delimited values'),
                code='bad_authorization_header',
            )

        return parts[1]

    @database_sync_to_async
    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken(_('Token contained no recognizable user identification'))

        try:
            user = self.user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except self.user_model.DoesNotExist:
            raise AuthenticationFailed(_('User not found'), code='user_not_found')

        if not user.is_active:
            raise AuthenticationFailed(_('User is inactive'), code='user_inactive')

        return user


def JWTMiddlewareStack(inner) -> JWTMiddleware:
    return JWTMiddleware(AuthMiddlewareStack(inner))