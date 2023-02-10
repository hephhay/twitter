from django.db.models import Manager

from utils.queryset import CustomQuerySet

class CustomManager(Manager): #type: ignore
    _queryset_class = CustomQuerySet