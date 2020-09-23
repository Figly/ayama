import datetime

from django import template
from django.db.models import DateField, ExpressionWrapper, F

from clients.models import ClientDetail
from practises.models import AdvisorDetail

register = template.Library()


@register.inclusion_tag("practises/advisors_list.html", takes_context=True)
def advisors_list(context, user):
    if user.is_administrator and user.is_advisor:
        advisors = AdvisorDetail.objects.filter(
            practise_id_fk=user.Advisor.practise_id_fk
        ).select_related("advisor_contact_fk")
        context = {"advisors": advisors}
    elif user.is_administrator:
        advisors = AdvisorDetail.objects.filter(
            practise_id_fk=user.Administrator.practise_id_fk
        ).select_related("advisor_contact_fk")
        context = {"advisors": advisors}
    elif user.is_superuser:
        advisors = AdvisorDetail.objects.all().select_related("advisor_contact_fk")
        context = {"advisors": advisors}

    return context
