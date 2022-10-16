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

    class Meta:
        ordering = ['created_at']
        abstract = True

class Post(BaseModel):
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

    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class Tweet(Post):

    def __str__(self) -> str:
        return f"Tweet, {self.id}, {self.created_by}"

class RelatePost(models.Model):

    def clean(self):
        """Ensure that only one of `reply` and `tweet` can be set."""
        if not (bool(self.reply) ^ bool(self.tweet)):
            raise ValidationError("Only one post field can be set.")

    reply = models.ForeignKey(
        'self',
        on_delete = models.CASCADE,
        related_name ='%(class)s_reply',
        null = True,
        editable=False
    )

    tweet = models.ForeignKey(
        Tweet,
        on_delete = models.CASCADE,
        related_name ='%(class)s_post',
        null = True,
        editable=False
    )

    class Meta:
        abstract = True

class Reply(Post, RelatePost):

    def __str__(self) -> str:
        return f"Reply, {self.id}, {self.created_by}"
