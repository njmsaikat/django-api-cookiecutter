from django.conf import settings
from django.db import models

from utils.models import CommonInfo


class Item(CommonInfo):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="items")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "example_item"
        ordering = ["-created_at"]
