from django.db.models import Manager

from utils.queryset import CustomQuerySet

class CustomManager(
    Manager.from_queryset(CustomQuerySet) #type: ignore
): ...
