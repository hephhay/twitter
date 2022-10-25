from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from rest_framework.exceptions import ValidationError

from uuid import uuid4

settings: any = settings
UserModel: str = settings.AUTH_USER_MODEL

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['-created_at', '-updated_at']
        abstract = True

class Tweet(BaseModel):
    likes = models.ManyToManyField(UserModel, related_name = '%(class)s_likes')

    content = models.TextField(_('content'), null = True)

    media = ArrayField(
        models.CharField(_('media files'), max_length = 200),
        default = list
    )

    created_by = models.ForeignKey(
        UserModel,
        on_delete = models.CASCADE,
        related_name = '%(class)s_creator',
        editable=False
    )

    reply = models.ForeignKey(
        'self',
        on_delete = models.CASCADE,
        related_name ='%(class)s_reply',
        null = True,
        editable=False
    )

    def __str__(self) -> str:
        return f"Tweet, {self.id}, {self.created_by}"

class ReTweet(BaseModel):
    quote = models.TextField(_('quote'), null = True)

    tweet = models.ForeignKey(
        Tweet,
        on_delete = models.CASCADE,
        related_name ='%(class)s_tweet',
        editable=False
    )

    created_by = models.ForeignKey(
        UserModel,
        on_delete = models.CASCADE,
        related_name = '%(class)s_creator',
        editable=False
    )
