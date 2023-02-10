from typing import Any

from rest_framework import viewsets, mixins

from real_time.models import Group, Message, Notification
from real_time.serilizers import (
    GroupSerializer,
    MessageSerializer,
    NotificationSerializer
)
from utils.permissions import OwnerOrAdminOrReadOnly
from utils.mixins import ViewSetMixins


class GroupViewSet(viewsets.ModelViewSet, ViewSetMixins):
    queryset = Group.objects.all()

    serializer_class = GroupSerializer

    permission_classes = [OwnerOrAdminOrReadOnly]

    owner_field = 'created_by'

    search_fields = ['group_name']

    def get_queryset(self) -> Any:
        queryset = super().get_queryset()

        if self.action == 'list':
            queryset = queryset.exclude(is_group=False)

        return queryset

    def list(self, request, *args, **kwargs):
        return self.generic_list(self.get_queryset())

class MessageViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    ViewSetMixins
):
    queryset = Message.objects.all()

    serializer_class = MessageSerializer

    permission_classes = [OwnerOrAdminOrReadOnly]

    owner_field = 'sender'

    search_fields = ['body']

class NotficationViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    ViewSetMixins
):
    queryset = Notification.objects.all()

    serializer_class = NotificationSerializer

    permission_classes = [OwnerOrAdminOrReadOnly]

    owner_field = 'sender'

    search_fields = ['user']