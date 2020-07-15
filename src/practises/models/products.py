from django.conf import settings
from django.db import models

from .base import BaseModel

types = (
    ("INS", "Insurance"),
    ("RA", "Retirement Annuity"),
    ("UT", "Unit Trust"),
)


class ProductDetail(BaseModel):
    """
    Class descriptor
    """

    product_type = models.CharField(
        "Product Type", max_length=30, choices=types, default="not specified"
    )
    product_name = models.CharField("Product Name", max_length=100)
    product_company = models.CharField("Product Company", max_length=100)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return f"{self.product_type} {self.product_name}"
