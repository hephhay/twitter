from uuid import uuid4
from os.path import splitext
import time

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from utils.queryset import CustomQuerySet

User_Model = settings.AUTH_USER_MODEL

def tweet_media_filename(instance, filename):
    __,extension = splitext(filename)
    return f'tweet/media/{instance.tweet.id}_{int(time.time())}{extension}'

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['-created_at', '-updated_at']
        abstract = True

class TweetQuerySet(CustomQuerySet):
        def prop_count(self):
            return self.num_one_to_many('retweet', 'reply')\
                .num_many_to_many('likes')\

class TweetManager(
    models.manager.BaseManager.from_queryset(TweetQuerySet) #type: ignore
): ...

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

    retweet = models.ForeignKey(
        'self',
        on_delete = models.CASCADE,
        related_name ='retweets',
        null = True,
        editable=False
    )

    reply = models.ForeignKey(
        'self',
        on_delete = models.CASCADE,
        related_name ='replies',
        null = True,
        editable=False
    )

    objects = TweetManager()

    def __str__(self) -> str:
        return f"Tweet, {self.id}, {self.created_by}"

class TweetMedia(models.Model):
    tweet = models.ForeignKey(
        Tweet,
        on_delete = models.CASCADE,
        editable = False
    )

    file = models.ImageField(
        _("tweet media file"),
        unique = True,
        upload_to = tweet_media_filename,
        editable = False
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
