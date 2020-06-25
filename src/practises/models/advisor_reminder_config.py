from django.conf import settings
from django.db import models

from .base import BaseModel


class AdvisorReminderConfig(BaseModel):
    """
    Class descriptor
    """
    face_to_face_frequency = models.IntegerField(blank=True, null=True, default=5)
    calls_frequency = models.IntegerField(blank=True, null=True, default=5)
    email_frequency = models.IntegerField(blank=True, null=True, default=5)
    sms_frequency = models.IntegerField(blank=True, null=True, default=5)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return f""
