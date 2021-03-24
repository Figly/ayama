from django.db import models

from .base import BaseModel


class ClientContactDetail(BaseModel):
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
        "Street Address", max_length=100
    )
    residential_address_line_2 = models.CharField(
        "Apt, Suite, Building or Company Name (Optional)", max_length=100, blank=True, null=True
    )
    residential_suburb = models.CharField(
        "Suburb", max_length=100, blank=True, null=True
    )
    residential_city = models.CharField(
        "City", max_length=100
    )
    residential_country = models.CharField(
        "Country", max_length=100, blank=True, null=True
    )
    residential_code = models.IntegerField("Postal Code")
    postal_address_line_1 = models.CharField("Street Address", max_length=100)
    postal_address_line_2 = models.CharField(
        "Apt, Suite, Building or Company Name (Optional)", max_length=100, blank=True, null=True
    )
    postal_suburb = models.CharField(
        "Suburb", max_length=100, blank=True, null=True
    )
    postal_city = models.CharField("Postal City", max_length=100, blank=True, null=True)
    postal_country = models.CharField(
        "Country", max_length=100, blank=True, null=True
    )
    postal_code = models.IntegerField("Postal Code")

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return f"{self.email_address}"
