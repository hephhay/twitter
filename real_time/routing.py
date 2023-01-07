from django.urls import re_path, path

from real_time.consumers import ChatConsumer, NotificatonConsumer

ws_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
    path("ws/notify/", NotificatonConsumer.as_asgi())
]