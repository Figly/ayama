from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .resources import ClientImportResource

from .models import (
    ClientCommunication,
    ClientContactDetail,
    ClientDetail,
    ClientImport,
    Dependent,
    EmploymentDetail,
    RatesAndReturn,
)


class ClientImportAdmin(ImportExportModelAdmin):
    resource_class = ClientImportResource
    pass


class ClientDetailsAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "initials",
        "surnames",
        "sa_id",
        "passport_no",
        "created_at",
        "modified_at",
    )


class ContactDetailsAdmin(admin.ModelAdmin):
    list_display = (
        "telephone_home",
        "telephone_work",
        "cellphone_number",
        "fax_number",
        "email_address",
        "created_at",
        "modified_at",
    )


class EmploymentDetailsAdmin(admin.ModelAdmin):
    list_display = (
        "company_name",
        "occupation",
        "employment_date",
        "personnel_number",
        "medical_aid",
        "retirement_fund_current_value",
        "group_life_cover",
        "created_at",
        "modified_at",
    )


class RatesAndReturnsAdmin(admin.ModelAdmin):
    list_display = (
        "inflation",
        "interest",
        "return_rate",
        "created_at",
        "modified_at",
    )


class DependentsAdmin(admin.ModelAdmin):
    list_display = (
        "names",
        "surnames",
        "rsa_resident",
        "id_no",
        "date_of_birth",
        "relationship",
    )


class ClientCommunicationsAdmin(admin.ModelAdmin):
    list_display = (
        "last_date_email",
        "last_date_sms",
        "last_date_call",
        "last_date_face_to_face",
    )


admin.site.register(ClientImport, ClientImportAdmin)
admin.site.register(ClientDetail, ClientDetailsAdmin)
admin.site.register(ClientContactDetail, ContactDetailsAdmin)
admin.site.register(EmploymentDetail, EmploymentDetailsAdmin)
admin.site.register(RatesAndReturn, RatesAndReturnsAdmin)
admin.site.register(Dependent, DependentsAdmin)
admin.site.register(ClientCommunication, ClientCommunicationsAdmin)
