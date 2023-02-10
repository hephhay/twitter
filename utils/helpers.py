from typing import Any, cast
from users.models import User


def cast_user(user: Any):
    return cast(User, user)