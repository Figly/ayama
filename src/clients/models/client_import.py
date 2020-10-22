from django.db import models

ch_medical_aid = (
    ("yes", "Yes"),
    ("no", "No"),
)
ch_group_life_cover = (
    ("yes", "Yes"),
    ("no", "No"),
)
ch_titles = (
    ("mr", "Mister"),
    ("mrs", "Misses"),
    ("ms", "Miss"),
    ("dr", "Doctor"),
    ("prof", "Professor"),
)


class ClientImport(models.Model):
    """
    A model which combines all Client fields which are required ,
    used for importing new clients and populating individual models
    """

    dateFormat = "%Y-%m-%d"
    advisor_email = models.EmailField("Advisor Email Address", max_length=50)
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

    company_name = models.CharField("Company Name", max_length=50)
    occupation = models.CharField("Occupation", max_length=50, blank=True, null=True)
    # employment_date = models.DateField(
    #     "Employment Date", auto_now=False, auto_now_add=False, default="2018-01-01"
    # )
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
        return f"{self.title} {self.initials} {self.surnames}"
