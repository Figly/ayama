import datetime

from clients.models import ClientDetail
from django import template
from django.db.models import DateField, ExpressionWrapper, F
from practises.models import AdvisorDetail

register = template.Library()


@register.inclusion_tag("clients/advisor_clients.html", takes_context=True)
def advisor_clients(context, user):
    if user.is_superuser:
        clients = ClientDetail.objects.all().select_related("client_contact_fk")
    elif user.is_administrator:
        practise_id = user.Administrator.practise_id_fk
        advisors = AdvisorDetail.objects.filter(practise_id_fk=practise_id)
        clients = ClientDetail.objects.filter(
            advisor_id_fk__in=advisors
        ).select_related("client_contact_fk")
    elif user.is_advisor:
        clients = ClientDetail.objects.filter(advisor_id_fk=user.id).select_related(
            "client_contact_fk"
        )

    context = {"clients": clients}
    return context
