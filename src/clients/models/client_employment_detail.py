from django.db import models

from .base import BaseModel

ch_medical_aid = (
    ("yes", "Yes"),
    ("no", "No"),
)
ch_group_life_cover = (
    ("yes", "Yes"),
    ("no", "No"),
)


class EmploymentDetail(BaseModel):
    """
    Class descriptor
    """

    dateFormat = "%Y-%m-%d"
    company_name = models.CharField("Company Name", max_length=50)
    occupation = models.CharField("Occupation", max_length=50, blank=True, null=True)
    employment_date = models.DateField(
        "Employment Date", auto_now=False, auto_now_add=False, default="2018-01-01"
    )
    personnel_number = models.CharField(
        "Personnel Number", max_length=50, blank=True, null=True
    )
    medical_aid = models.CharField(
        "Medical Aid", max_length=5, choices=ch_medical_aid, default="no"
    )
    retirement_fund_current_value = models.DecimalField(
        "Retirement Fund Current Value",
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
    )
    group_life_cover = models.CharField(
        "Group Life Cover", max_length=5, choices=ch_group_life_cover, default="no"
    )

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return f"{self.client_id_fk} - {self.company_name} - {self.occupation}"