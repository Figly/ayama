from django.db import models

from .base import BaseModel


class RatesAndReturn(BaseModel):
    """
    Class descriptor
    """

    inflation = models.DecimalField(
        "Inflation", max_digits=5, decimal_places=2, blank=True, null=True
    )
    interest = models.DecimalField(
        "Interest", max_digits=5, decimal_places=2, blank=True, null=True
    )
    return_rate = models.DecimalField(
        "Return Rate", max_digits=5, decimal_places=2, blank=True, null=True
    )

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return f"{self.inflation} - {self.interest}"
