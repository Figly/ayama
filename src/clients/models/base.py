from datetime import datetime

from django.conf import settings
from django.db import models
from django.utils.timezone import get_current_timezone


class BaseModel(models.Model):
    dateFormat = "%Y-%m-%d %H:%M:%S"

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    class Meta:
        get_latest_by = "created_at"
        order_with_respect_to = "created_at"
        abstract = True

    @property
    def created(self):
        return datetime.strftime(
            self.created_at.astimezone(get_current_timezone()), self.dateFormat
        )

    @property
    def modified(self):
        return datetime.strftime(
            self.modified_at.astimezone(get_current_timezone()), self.dateFormat
        )