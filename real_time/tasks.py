from typing import Optional

from uuid import UUID
from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from celery import group

from twitter.celery import app
from twitter.consumers import BaseConsumer
from real_time.models import Clients

@app.task
def send_notification(user_id: UUID) -> None:
    chanels = Clients.objects.filter(user = user_id)\
        .values_list('channel_name', flat=True)
    print(chanels)

@app.task
def notify_channel(channel_id: str)-> None:
    channel_layer: Optional[BaseConsumer] = get_channel_layer()

    if channel_layer:
        async_to_sync(channel_layer.send)(channel_id, {
            "type": "notify_user",
            "message": "happy"
        })
