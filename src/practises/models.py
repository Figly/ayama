from datetime import datetime
from django.utils.timezone import get_current_timezone

from django.db import models

ch_titles = (
    ('mr', 'Mister'),
    ('mrs', 'Misses'),
    ('ms', 'Miss'),
    ('dr', 'Doctor'),
    ('prof', 'Professor'),
)


class BaseModel(models.Model):
    dateFormat = '%Y-%m-%d %H:%M:%S'

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = 'created_at'
        order_with_respect_to = 'created_at'
        abstract = True

    @property
    def created(self):
        return datetime.strftime(self.created_at.astimezone(get_current_timezone()), self.dateFormat)

    @property
    def modified(self):
        return datetime.strftime(self.modified_at.astimezone(get_current_timezone()), self.dateFormat)


class PractiseDetail(BaseModel):
    """
    Class descriptor
    """
    dateFormat = '%Y-%m-%d'

    name = models.CharField('Practise Name', max_length=100)
    residential_address_line_1 = models.CharField('Residential Address 1', max_length=100)
    residential_address_line_2 = models.CharField('Residential Address 2', max_length=100, blank=True, null=True)
    residential_code = models.IntegerField('Residential Code')
    postal_address_line_1 = models.CharField('Postal Address 1', max_length=100)
    postal_address_line_2 = models.CharField('Postal Address 2', max_length=100, blank=True, null=True)
    postal_code = models.IntegerField('Postal Code')

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return f'{self.name}'


class AdministratorDetail(BaseModel):
    """
    Class descriptor
    """

    practise_id_fk = models.ForeignKey('PractiseDetail', on_delete=models.CASCADE)
    advisor_id_fk = models.ForeignKey('AdvisorDetail', on_delete=models.CASCADE)
    title = models.CharField('Title', max_length=30, choices=ch_titles, default='not specified')
    initials = models.CharField('Initials', max_length=10)
    surnames = models.CharField('Surnames', max_length=100)
    names = models.CharField('Names', max_length=100)
    known_as = models.CharField('Known As', max_length=50, blank=True, null=True)
    sa_id = models.BigIntegerField('RSA ID Number')
    passport_no = models.CharField('Passport Number', max_length=50, blank=True, null=True)
    position = models.CharField('Position', max_length=50, blank=True, null=True)
    employment_date = models.DateField('Employment Date', auto_now=False, auto_now_add=False)
    personnel_number = models.CharField('Personnel Number', max_length=50, blank=True, null=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return f'{self.get_title_display()} {self.initials} {self.surnames}'


class AdvisorDetail(BaseModel):
    """
    Class descriptor
    """

    practise_id_fk = models.ForeignKey('PractiseDetail', on_delete=models.CASCADE)
    title = models.CharField('Title', max_length=30, choices=ch_titles, default='not specified')
    initials = models.CharField('Initials', max_length=10)
    surnames = models.CharField('Surnames', max_length=100)
    names = models.CharField('Names', max_length=100)
    known_as = models.CharField('Known As', max_length=50, blank=True, null=True)
    sa_id = models.BigIntegerField('RSA ID Number')
    passport_no = models.CharField('Passport Number', max_length=50, blank=True, null=True)
    position = models.CharField('Position', max_length=50, blank=True, null=True)
    employment_date = models.DateField('Employment Date', auto_now=False, auto_now_add=False)
    personnel_number = models.CharField('Personnel Number', max_length=50, blank=True, null=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return f'{self.get_title_display()} {self.initials} {self.surnames}'


class AdvisorContactDetail(BaseModel):
    """
    Class descriptor
    """

    advisor_id_fk = models.ForeignKey('AdvisorDetail', on_delete=models.CASCADE)
    telephone_home = models.CharField('Home Telephone Number', max_length=10, blank=True, null=True)
    telephone_work = models.CharField('Work Telephone Number', max_length=10, blank=True, null=True)
    cellphone_number = models.CharField('Cellphone Number', max_length=10)
    fax_number = models.CharField('Fax Number', max_length=10, blank=True, null=True)
    email_address = models.CharField('Email Address', max_length=50)
    residential_address_line_1 = models.CharField('Residential Address 1', max_length=100)
    residential_address_line_2 = models.CharField('Residential Address 2', max_length=100, blank=True, null=True)
    residential_code = models.IntegerField('Residential Code')
    postal_address_line_1 = models.CharField('Postal Address 1', max_length=100)
    postal_address_line_2 = models.CharField('Postal Address 2', max_length=100, blank=True, null=True)
    postal_code = models.IntegerField('Postal Code')

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return f'{self.advisor_id_fk} {self.email_address}'


class AdministratorContactDetail(BaseModel):
    """
    Class descriptor
    """

    adminstrator_id_fk = models.ForeignKey('AdministratorDetail', on_delete=models.CASCADE)
    telephone_home = models.CharField('Home Telephone Number', max_length=10, blank=True, null=True)
    telephone_work = models.CharField('Work Telephone Number', max_length=10, blank=True, null=True)
    cellphone_number = models.CharField('Cellphone Number', max_length=10)
    fax_number = models.CharField('Fax Number', max_length=10, blank=True, null=True)
    email_address = models.CharField('Email Address', max_length=50)
    residential_address_line_1 = models.CharField('Residential Address 1', max_length=100)
    residential_address_line_2 = models.CharField('Residential Address 2', max_length=100, blank=True, null=True)
    residential_code = models.IntegerField('Residential Code')
    postal_address_line_1 = models.CharField('Postal Address 1', max_length=100)
    postal_address_line_2 = models.CharField('Postal Address 2', max_length=100, blank=True, null=True)
    postal_code = models.IntegerField('Postal Code')

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return f'{self.adminstrator_id_fk} {self.email_address}'
