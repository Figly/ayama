from django.conf import settings
from django.db import models

from .base import BaseModel

ch_titles = (
    ("mr", "Mister"),
    ("mrs", "Misses"),
    ("ms", "Miss"),
    ("dr", "Doctor"),
    ("prof", "Professor"),
)


class AdministratorDetail(BaseModel):
    """
    Class descriptor
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="Administrator",
    )
    practise_id_fk = models.ForeignKey(
        "PractiseDetail", on_delete=models.CASCADE, related_name="Practise"
    )
    adminstrator_contact_fk = models.ForeignKey(
        "AdministratorContactDetail", on_delete=models.CASCADE
    )
    title = models.CharField(
        "Title", max_length=30, choices=ch_titles, default="not specified"
    )
    initials = models.CharField("Initials", max_length=10)
    surnames = models.CharField("Surnames", max_length=100)
    names = models.CharField("Names", max_length=100)
    known_as = models.CharField("Known As", max_length=50, blank=True, null=True)
    sa_id = models.BigIntegerField("RSA ID Number")
    passport_no = models.CharField(
        "Passport Number", max_length=50, blank=True, null=True
    )
    position = models.CharField("Position", max_length=50, blank=True, null=True)
    employment_date = models.DateField(
        "Employment Date", auto_now=False, auto_now_add=False, default="2018-01-01"
    )
    personnel_number = models.CharField(
        "Personnel Number", max_length=50, blank=True, null=True
    )

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return f"{self.get_title_display()} {self.initials} {self.surnames}"
