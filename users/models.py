from django.db import models
from django.contrib.auth import models as AuthModels
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

from uuid import uuid4

class User(AuthModels.AbstractUser):    #type:ignore
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with this email already exists."),
        },
        validators=[validate_email]
    )

    first_name = models.CharField(_("first name"), max_length=150)

    last_name = models.CharField(_("last name"), max_length=150)

    avatar = models.CharField(_("profile pictire"), max_length = 100, null=True)

    location = models.CharField(_("location"), max_length = 100)

    birth_date = models.DateField(_("birthday"))

    is_verified = models.BooleanField(default = False)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    updated_at = models.DateTimeField(auto_now=True, editable=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.email}, {self.username}"

    class Meta:
        ordering = ['-created_at']
