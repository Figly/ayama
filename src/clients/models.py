from datetime import datetime

from django.db import models
from django.utils.timezone import get_current_timezone

ch_titles = (
    ("mr", "Mister"),
    ("mrs", "Misses"),
    ("ms", "Miss"),
    ("dr", "Doctor"),
    ("prof", "Professor"),
)

ch_medical_aid = (
    ("yes", "Yes"),
    ("no", "No"),
)
ch_group_life_cover = (
    ("yes", "Yes"),
    ("no", "No"),
)
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


class BaseModel(models.Model):
    dateFormat = "%Y-%m-%d %H:%M:%S"

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = "created_at"
        order_with_respect_to = "created_at"
        abstract = True

    @property
    def created(self):
        return datetime.strftime(
            self.created_at.astimezone(get_current_timezone()), self.dateFormat
        )

    @property
    def modified(self):
        return datetime.strftime(
            self.modified_at.astimezone(get_current_timezone()), self.dateFormat
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
        "Residential Address 1", max_length=100
    )
    residential_address_line_2 = models.CharField(
        "Residential Address 2", max_length=100, blank=True, null=True
    )
    residential_code = models.IntegerField("Residential Code")
    postal_address_line_1 = models.CharField("Postal Address 1", max_length=100)
    postal_address_line_2 = models.CharField(
        "Postal Addres 2", max_length=100, blank=True, null=True
    )
    postal_code = models.IntegerField("Postal Code")

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return f"{self.client_id_fk} - {self.email_address}"


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
        return f"{self.client_id_fk}"


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


class ClientCommunication(BaseModel):
    """
    Class descriptor
    """
    last_date_email = models.DateField(
        "Last date email", auto_now=False, auto_now_add=False, default=None, blank=True, null=True
    )

    last_date_sms = models.DateField(
        "Last date SMS", auto_now=False, auto_now_add=False, default=None, blank=True, null=True
    )
    last_date_call = models.DateField(
        "Last date call", auto_now=False, auto_now_add=False, default=None, blank=True, null=True
    )
    last_date_face_to_face = models.DateField(
        "Last date face to face", auto_now=False, auto_now_add=False, default=None, blank=True, null=True
    )
    def __str__(self):
        """Return a human readable representation of the model instance."""
        return f"{self.names} {self.surnames}"
