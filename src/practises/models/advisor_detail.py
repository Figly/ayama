from django.conf import settings
from django.db import models

from .advisor_reminder_config import AdvisorReminderConfig
from .base import BaseModel

ch_titles = (
    ("mr", "Mister"),
    ("mrs", "Misses"),
    ("ms", "Miss"),
    ("dr", "Doctor"),
    ("prof", "Professor"),
)


class AdvisorDetail(BaseModel):

    """
    Class descriptor
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="Advisor",
    )
    practise_id_fk = models.ForeignKey(
        "PractiseDetail",
        on_delete=models.CASCADE,
        related_name="Advisors",
        null=True,
        default=None,
    )
    advisor_contact_fk = models.ForeignKey(
        "AdvisorContactDetail", on_delete=models.CASCADE
    )
    advisor_employment_fk = models.ForeignKey(
        "AdvisorEmploymentDetail", on_delete=models.CASCADE
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

    reminder_config_freq_fk = models.ForeignKey(
        "AdvisorReminderConfig",
        on_delete=models.CASCADE,
        related_name="reminder_config",
    )

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return f"{self.get_title_display()} {self.initials} {self.surnames}"
