from datetime import datetime, timedelta

from clients.models import ClientDetail
from django import template
from django.db.models import DateField, ExpressionWrapper, F, Q
from practises.models import AdvisorDetail

register = template.Library()


@register.inclusion_tag("clients/client_scheduler.html", takes_context=True)
def client_scheduler(context, user):
    if user.is_advisor:
        clients = ClientDetail.objects.filter(advisor_id_fk=user.id)
        over_due = clients.filter(
            client_comms_fk__last_contacted__lte=datetime.now() - timedelta(days=180)
        )
        due = clients.filter(
            Q(
                client_comms_fk__last_contacted__gte=datetime.now()
                - timedelta(days=180)
            ),
            Q(
                client_comms_fk__last_contacted__lte=datetime.now()
                - timedelta(days=150)
            ),
        )
        happy = clients.filter(
            client_comms_fk__last_contacted__gte=datetime.now() - timedelta(days=150)
        )
    elif user.is_administrator:

        practise_id = user.Administrator.practise_id_fk
        advisors = AdvisorDetail.objects.filter(practise_id_fk=practise_id)
        clients = ClientDetail.objects.filter(advisor_id_fk__in=advisors)

        over_due = clients.filter(
            client_comms_fk__last_contacted__lte=datetime.now() - timedelta(days=180)
        )
        due = clients.filter(
            Q(
                client_comms_fk__last_contacted__gte=datetime.now()
                - timedelta(days=180)
            ),
            Q(
                client_comms_fk__last_contacted__lte=datetime.now()
                - timedelta(days=150)
            ),
        )
        happy = clients.filter(
            client_comms_fk__last_contacted__gte=datetime.now() - timedelta(days=150)
        )

    context = {"over_due": over_due.count(), "due": due.count(), "happy": happy.count()}
    return context
