from django.contrib import admin
from .models import ClientDetail, ClientContactDetail, EmploymentDetail, RatesAndReturn, Dependent


class ClientDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'initials',
        'surnames',
        'sa_id',
        'passport_no',
        'created_at',
        'modified_at',
    )


class ContactDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'telephone_home',
        'telephone_work',
        'cellphone_number',
        'fax_number',
        'email_address',
        'created_at',
        'modified_at',
    )


class EmploymentDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'company_name',
        'occupation',
        'employment_date',
        'personnel_number',
        'medical_aid',
        'retirement_fund_current_value',
        'group_life_cover',
        'created_at',
        'modified_at',
    )


class RatesAndReturnsAdmin(admin.ModelAdmin):
    list_display = (
        'inflation',
        'interest',
        'return_rate',
        'created_at',
        'modified_at',
    )


class DependentsAdmin(admin.ModelAdmin):
    list_display = (
        'names',
        'surnames',
        'rsa_resident',
        'id_no',
        'date_of_birth',
        'relationship',
    )


admin.site.register(ClientDetail, ClientDetailsAdmin)
admin.site.register(ClientContactDetail, ContactDetailsAdmin)
admin.site.register(EmploymentDetail, EmploymentDetailsAdmin)
admin.site.register(RatesAndReturn, RatesAndReturnsAdmin)
admin.site.register(Dependent, DependentsAdmin)
