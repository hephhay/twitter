from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from post.models import BaseModel

class Group(BaseModel):
    group_name = models.CharField(
        _("group name"),
        max_length = 50,
        unique = True
    )
    
    participants = models.ManyToManyField(get_user_model())

class Message(BaseModel):
    body = models.TextField(_('body'))

    is_document = models.BooleanField(default = False)

    sender = models.ForeignKey(
        get_user_model(),
        on_delete = models.CASCADE,
        related_name = '%(class)s_user',
        editable=False
    )

    group =models.ForeignKey(
        Group,
        on_delete = models.CASCADE,
        editable=False
    )

    seen_by = models.ManyToManyField(get_user_model())

