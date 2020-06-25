from django.db import models

from .base import BaseModel

ch_titles = (
    ("mr", "Mister"),
    ("mrs", "Misses"),
    ("ms", "Miss"),
    ("dr", "Doctor"),
    ("prof", "Professor"),
)


class ClientDetail(BaseModel):
    """
    Class descriptor
    """

    advisor_id_fk = models.ForeignKey(
        "practises.AdvisorDetail", on_delete=models.CASCADE, related_name="clients"
    )
    client_contact_fk = models.ForeignKey(
        "ClientContactDetail", on_delete=models.CASCADE
    )
    title = models.CharField(
        "Title", max_length=30, choices=ch_titles, default="not specified"
    )
    initials = models.CharField("Initials", max_length=10)
    surnames = models.CharField("Surname", max_length=100)
    names = models.CharField("Name", max_length=100)
    known_as = models.CharField("Known As", max_length=50, blank=True, null=True)
    sa_id = models.BigIntegerField("RSA ID Number")
    passport_no = models.CharField(
        "Passport Number", max_length=50, blank=True, null=True
    )
    client_employment_fk = models.ForeignKey(
        "EmploymentDetail", on_delete=models.CASCADE
    )
    client_rates_fk = models.ForeignKey("RatesAndReturn", on_delete=models.CASCADE)
    client_comms_fk = models.ForeignKey("ClientCommunication", on_delete=models.CASCADE)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return f"{self.get_title_display()} {self.initials} {self.surnames}"
