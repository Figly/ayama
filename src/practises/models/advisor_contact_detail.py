from django.conf import settings
from django.db import models

from .base import BaseModel


class AdvisorContactDetail(BaseModel):
    """
    Class descriptor
    """

    telephone_home = models.CharField(
        "Home Telephone Number", max_length=10, blank=True, null=True
    )
    telephone_work = models.CharField(
        "Work Telephone Number", max_length=10, blank=True, null=True
    )
    cellphone_number = models.CharField("Cellphone Number", max_length=10)
    fax_number = models.CharField("Fax Number", max_length=10, blank=True, null=True)
    email_address = models.EmailField("Email Address", max_length=50)
    residential_address_line_1 = models.CharField(
        "Residential Address Line 1", max_length=100
    )
    residential_address_line_2 = models.CharField(
        "Residential Address Line 2", max_length=100, blank=True, null=True
    )
    residential_suburb = models.CharField(
        "Residential Suburb", max_length=100, blank=True, null=True
    )
    residential_city = models.CharField(
        "Residential City", max_length=100, blank=True, null=True
    )
    residential_country = models.CharField(
        "Residential Country", max_length=100, blank=True, null=True
    )
    residential_code = models.IntegerField("Residential Code")
    postal_address_line_1 = models.CharField("Postal Address Line 1", max_length=100)
    postal_address_line_2 = models.CharField(
        "Postal Address Line 2", max_length=100, blank=True, null=True
    )
    postal_suburb = models.CharField(
        "Postal Suburb", max_length=100, blank=True, null=True
    )
    postal_city = models.CharField("Postal City", max_length=100, blank=True, null=True)
    postal_country = models.CharField(
        "Postal Country", max_length=100, blank=True, null=True
    )
    postal_code = models.IntegerField("Postal Code")

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return f"{self.email_address}"
