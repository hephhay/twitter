"""
ASGI config for twitter project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from twitter.middleware import JWTMiddlewareStack

import twitter.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twitter.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": application,
    "websocket": AllowedHostsOriginValidator(
        JWTMiddlewareStack(URLRouter(twitter.routing.websocket_urlpatterns))
        ),
})
