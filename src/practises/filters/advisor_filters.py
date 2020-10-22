import django_filters

from ..models import AdvisorContactDetail, AdvisorDetail


class AdvisorFilter(django_filters.FilterSet):
    email_address = django_filters.CharFilter(
        field_name="advisor_contact_fk__email_address", lookup_expr="contains"
    )
    surnames = django_filters.CharFilter(field_name="surnames", lookup_expr="contains")
    names = django_filters.CharFilter(field_name="names", lookup_expr="contains")

    class Meta:
        model = AdvisorDetail
        fields = [
            "surnames",
            "names",
            "email_address",
        ]
