from django.db import models

from .base import BaseModel

ch_rsa_resident = (
    ("yes", "Yes"),
    ("no", "No"),
)
ch_relationship = (
    ("mother", "Mother"),
    ("father", "Father"),
    ("brother", "Brother"),
    ("sister", "Sister"),
    ("grandfather", "Grandfather"),
    ("grandmother", "Grandmother"),
    ("father_in_law", "Father-in-Law"),
    ("mother_in_law", "Mother-in-Law"),
    ("other", "Other"),
)


class Dependent(BaseModel):
    """
    Class descriptor
    """

    client_id_fk = models.ForeignKey(
        "ClientDetail", on_delete=models.CASCADE, related_name="dependents"
    )
    dateFormat = "%Y-%m-%d"
    names = models.CharField("Name", max_length=100)
    surnames = models.CharField("Surname", max_length=100)
    rsa_resident = models.CharField(
        "RSA Resident", max_length=5, choices=ch_rsa_resident, default="yes"
    )
    id_no = models.IntegerField("RSA ID Number")
    date_of_birth = models.DateField(
        "Date of Birth", auto_now=False, auto_now_add=False
    )
    relationship = models.CharField(
        "Relationship", max_length=50, choices=ch_relationship, default="not specified"
    )
    other = models.CharField("Other", max_length=100, blank=True, null=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return f"{self.names} {self.surnames}"