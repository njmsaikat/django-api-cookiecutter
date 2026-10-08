from django.db import models


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True


class CommonInfo(TimeStamp):
    """TimeStamp plus an `is_active` flag (defaults to False)."""

    is_active = models.BooleanField(default=False)

    class Meta:
        abstract = True
