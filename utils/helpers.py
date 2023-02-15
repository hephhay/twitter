from typing import Any, cast

from django.utils.translation import gettext_lazy as _
from django.core.files.uploadedfile import UploadedFile
from django.conf import settings

from rest_framework.exceptions import ValidationError

from users.models import User

setting: Any = settings

max_image_file = setting.MAX_IMAGE_SIZE

def cast_user(user: Any):
    return cast(User, user)

def validate_image(image: UploadedFile, max_size = max_image_file):
    if image.size > max_size:
        max_image = f'{max_size // (1024 ** 2)}MB'
        raise ValidationError(
            _(f"File too large max size is {max_image}")
        )
