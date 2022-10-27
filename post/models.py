from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from uuid import uuid4

User = settings.AUTH_USER_MODEL

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['-created_at', '-updated_at']
        abstract = True

class Post(BaseModel):

    likes = models.ManyToManyField(User, related_name = '%(class)s_likes')

    content = models.TextField(_('content'), null = True)

    media = ArrayField(
        models.CharField(_('media files'), max_length = 200),
        default = list
    )

    created_by = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = '%(class)s_creator',
        editable=False
    )

    class Meta:
        abstract = True

class Tweet(Post):

    reply = models.ForeignKey(
        'self',
        on_delete = models.CASCADE,
        related_name ='%(class)s_reply',
        null = True,
        editable=False
    )

    is_reply = models.BooleanField(
        _('is reply'),
        default = False,
        editable = False
    )

    def save(self, *args, **kwargs) -> None:
        if (self.reply or self.reply_id):
            self.is_reply = True
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Tweet, {self.id}, {self.created_by}"

class ReTweet(Post):

    tweet = models.ForeignKey(
        Tweet,
        on_delete = models.CASCADE,
        related_name ='%(class)s_tweet',
        editable=False
    )

    created_by = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = '%(class)s_creator',
        editable=False
    )

    def __str__(self) -> str:
        return f"Re_Tweet, {self.id}, {self.created_by}"
