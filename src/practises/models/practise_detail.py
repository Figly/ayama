from django.conf import settings
from django.db import models

from .base import BaseModel


class PractiseDetail(BaseModel):
    """
    Class descriptor
    """

    dateFormat = "%Y-%m-%d"

    name = models.CharField("Practise Name", max_length=100)
    residential_address_line_1 = models.CharField(
        "Residential Address 1", max_length=100
    )
    residential_address_line_2 = models.CharField(
        "Residential Address 2", max_length=100, blank=True, null=True
    )
    residential_code = models.IntegerField("Residential Code")
    postal_address_line_1 = models.CharField("Postal Address 1", max_length=100)
    postal_address_line_2 = models.CharField(
        "Postal Address 2", max_length=100, blank=True, null=True
    )
    postal_code = models.IntegerField("Postal Code")

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return f"{self.name}"
