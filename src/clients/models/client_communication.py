from django.db import models

from .base import BaseModel


class ClientCommunication(BaseModel):
    """
    Class descriptor
    """
    last_date_email = models.DateField(
        "Last date email", auto_now=False, auto_now_add=False, default=None, blank=True, null=True
    )

    last_date_sms = models.DateField(
        "Last date SMS", auto_now=False, auto_now_add=False, default=None, blank=True, null=True
    )
    last_date_call = models.DateField(
        "Last date call", auto_now=False, auto_now_add=False, default=None, blank=True, null=True
    )
    last_date_face_to_face = models.DateField(
        "Last date face to face", auto_now=False, auto_now_add=False, default=None, blank=True, null=True
    )
    def __str__(self):
        """Return a human readable representation of the model instance."""
        return f"{self.names} {self.surnames}"


class ClientCommunicationFrequency(BaseModel):
    """
    Class descriptor
    """
    face_to_face_frequency = models.IntegerField(blank=True, null=True)
    calls_frequency = models.IntegerField(blank=True, null=True)
    email_frequency = models.IntegerField(blank=True, null=True)
    sms_frequency = models.IntegerField(blank=True, null=True)
    def __str__(self):
        """Return a human readable representation of the model instance."""
        return f"{self.names} {self.surnames}"
