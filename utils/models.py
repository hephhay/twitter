from uuid import uuid4
from django.db import models

# Create your models here.

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['-created_at', '-updated_at']
        abstract = True