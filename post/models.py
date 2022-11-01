from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from uuid import uuid4

User_Model = settings.AUTH_USER_MODEL

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['-created_at', '-updated_at']
        abstract = True

class Like(models.Model):
    liked_by = models.ForeignKey(
        User_Model,
        on_delete = models.CASCADE,
        editable = False,
    )

    liked = models.ForeignKey(
        'Tweet',
        on_delete = models.CASCADE,
        editable = False,
    )

    liked_on = models.DateTimeField(
        auto_now_add = True,
        editable = False
    )

class Tweet(BaseModel):

    likes = models.ManyToManyField(
        User_Model,
        through = 'Like',
        through_fields = ('liked', 'liked_by'),
        related_name = 'user_likes'
    )

    content = models.TextField(_('content or quote'), null = True)

    tags = ArrayField(
        models.CharField(_('hash tags or usernames'), max_length = 200),
        default = list
    )

    media = ArrayField(
        models.CharField(_('media files'), max_length = 200),
        default = list
    )

    created_by = models.ForeignKey(
        User_Model,
        on_delete = models.CASCADE,
        editable=False
    )

    tweet = models.ForeignKey(
        'self',
        on_delete = models.CASCADE,
        related_name ='retweets',
        null = True,
        editable=False
    )

    reply_to = models.ForeignKey(
        'self',
        on_delete = models.CASCADE,
        related_name ='replies',
        null = True,
        editable=False
    )

    def __str__(self) -> str:
        return f"Tweet, {self.id}, {self.created_by}"
