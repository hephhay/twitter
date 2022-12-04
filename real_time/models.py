from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from post.models import BaseModel
from users.models import Owned, RelateTweet

class Group(BaseModel):
    group_name = models.CharField(
        _("group name"),
        max_length=50,
        unique=True
    )

    description = models.CharField(
        _('Group Description'),
        max_length=256,
        null=True,
        blank=True
    )

    is_group = models.BooleanField(
        _('is group'),
        default=False
    )

    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='%(class)s_creator',
        editable=False
    )

    participants = models.ManyToManyField(get_user_model())

class Message(BaseModel):
    body = models.TextField(_('body'))

    is_document = models.BooleanField(default = False)

    sender = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='%(class)s_user',
        editable=False
    )

    group =models.ForeignKey(
        Group,
        on_delete = models.CASCADE,
        editable=False
    )

    seen_by = models.ManyToManyField(get_user_model())

class Notification(BaseModel, Owned, RelateTweet): #type: ignore
    body = models.TextField(_('body'))
    seen = models.BooleanField(default = False)

    def __str__(self):
        return f"Notification, {self.id}, {self.user}, {self.body}"
