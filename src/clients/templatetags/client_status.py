from datetime import datetime, timedelta

from django import template

register = template.Library()


@register.simple_tag
def client_status(last_contacted):

    last_contacted_date = datetime(
        last_contacted.year, last_contacted.month, last_contacted.day
    )
    overdue_cutoff = datetime(
        (datetime.now() - timedelta(days=180)).year,
        (datetime.now() - timedelta(days=180)).month,
        (datetime.now() - timedelta(days=180)).day,
    )
    due_cuttoff = datetime(
        (datetime.now() - timedelta(days=150)).year,
        (datetime.now() - timedelta(days=150)).month,
        (datetime.now() - timedelta(days=150)).day,
    )

    if last_contacted_date < overdue_cutoff:
        return "Overdue"
    elif (
        last_contacted_date > overdue_cutoff
        and datetime(last_contacted.year, last_contacted.month, last_contacted.day)
        < due_cuttoff
    ):
        return "Due"
    elif last_contacted_date > due_cuttoff:
        return "Happy"
