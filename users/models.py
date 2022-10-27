from uuid import uuid4

from django.db import models
from django.contrib.auth import models as AuthModels
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

from post.models import BaseModel, Tweet, User as User_Model

class Follow(models.Model):
    user = models.ForeignKey(
        User_Model,
        on_delete = models.CASCADE,
        editable = False,
        related_name = 'follow_user'
    )

    follower = models.ForeignKey(
        User_Model,
        on_delete = models.CASCADE,
        editable = False,
    )

    start_follow = models.DateTimeField(
        auto_now_add = True,
        editable = False
    )

class User(AuthModels.AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4, editable=False
    )

    email = models.EmailField(
        _("email address"),
        unique = True,
        error_messages = {
            "unique": _("A user with this email already exists."),
        },
        validators=[validate_email]
    )

    first_name = models.CharField(_("first name"), max_length=150)

    last_name = models.CharField(_("last name"), max_length=150)

    followers = models.ManyToManyField(
        'self',
        through='Follow',
        through_fields=('user', 'follower'),
        related_name = 'following',
        symmetrical = False
    )

    avatar = models.CharField(
        _("profile pictire"),
        max_length = 100,
        null=True
    )

    location = models.CharField(
        _("location"),
        max_length = 100,
        null = True
    )

    birth_date = models.DateField(_("birthday"))

    is_verified = models.BooleanField(default = False)

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
        "birth_date"
    ]

    def __str__(self):
        return f"User, {self.email}, {self.username}"

    class Meta:
        ordering = ['-created_at']

class Owned(models.Model):
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = '%(class)s_user',
        editable=False
    )
    class Meta:
        abstract = True

class RelateTweet(models.Model):
    tweet = models.ForeignKey(
        Tweet,
        on_delete = models.CASCADE,
        related_name ='%(class)s_tweet',
        null = True,
        editable=False
    )
    class Meta:
        abstract = True

class Notification(BaseModel, Owned, RelateTweet):
    body = models.TextField(_('body'))
    seen = models.BooleanField(default = False)

    def __str__(self):
        return f"Notification, {self.id}, {self.user}, {self.body}"

class Bookmark(BaseModel, Owned, RelateTweet):

    def __str__(self):
        return f"Bookmark, {self.id}"
