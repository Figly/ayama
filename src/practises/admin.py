from django.contrib import admin

from .models import (AdministratorContactDetail, AdministratorDetail,
                     AdvisorContactDetail, AdvisorDetail, PractiseDetail)


class PractiseDetailAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'residential_address_line_1',
        'residential_address_line_2',
        'residential_code',
        'postal_address_line_1',
        'postal_address_line_2',
        'postal_code',
    )


class AdvisorDetailAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'initials',
        'surnames',
        'names',
        'known_as',
        'sa_id',
        'passport_no',
        'position',
        'employment_date',
        'personnel_number',
    )


class AdvisorContactDetailAdmin(admin.ModelAdmin):
    list_display = (
        'telephone_home',
        'telephone_work',
        'cellphone_number',
        'fax_number',
        'email_address',
        'residential_address_line_1',
        'residential_address_line_2',
        'residential_code',
        'postal_address_line_1',
        'postal_address_line_2',
        'postal_code',
    )


class AdministratorDetailAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'initials',
        'surnames',
        'names',
        'known_as',
        'sa_id',
        'passport_no',
        'position',
        'employment_date',
        'personnel_number',
    )


class AdministratorContactDetailAdmin(admin.ModelAdmin):
    list_display = (
        'telephone_home',
        'telephone_work',
        'cellphone_number',
        'fax_number',
        'email_address',
        'residential_address_line_1',
        'residential_address_line_2',
        'residential_code',
        'postal_address_line_1',
        'postal_address_line_2',
        'postal_code',
    )


admin.site.register(PractiseDetail, PractiseDetailAdmin)
admin.site.register(AdvisorDetail, AdvisorDetailAdmin)
admin.site.register(AdvisorContactDetail, AdvisorContactDetailAdmin)
admin.site.register(AdministratorDetail, AdministratorDetailAdmin)
admin.site.register(AdministratorContactDetail, AdministratorContactDetailAdmin)
