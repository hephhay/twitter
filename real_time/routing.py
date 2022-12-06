from django.urls import re_path

from real_time.consumers import ChatConsumer

ws_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
]