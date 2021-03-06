from django.conf import settings
from django.db import models

from .base import BaseModel


class AdvisorEmploymentDetail(BaseModel):

    """
    Class descriptor
    """

    position = models.CharField("Position", max_length=50, blank=True, null=True)
    employment_date = models.DateField(
        "Employment Date", auto_now=False, auto_now_add=False
    )
    personnel_number = models.CharField(
        "Personnel Number", max_length=50, blank=True, null=True
    )

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return f"{self.get_title_display()} {self.personnel_number}"
