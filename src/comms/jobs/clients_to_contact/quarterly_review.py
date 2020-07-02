"""
Sample email send invocation using the Django email backend setup (hooked up to Sendgrid)
"""
import logging
from datetime import datetime, timedelta

import django
from django.core.mail import send_mail, send_mass_mail
from django.db.models import Q

from clients.models.client_communication import ClientCommunication
from practises.models.advisor_contact_detail import AdvisorContactDetail
from practises.models.advisor_detail import AdvisorDetail

log = logging.getLogger(__name__)


def run(**kwargs):
    django.setup()
    try:
        today = datetime.today()
        three_months_ago = today - timedelta(days=3)

        _subject = kwargs["subject"] or "Communication Reminder"
        _body = kwargs["body"] or "Communication reminder job run."
        _from = kwargs["from"] or "karelverhoeven@gmail.com"
        _to = (
            kwargs["to"]
            or "kylebrandin@gmail.com,karelverhoeven@gmail.com,coetzee.vs@gmail.com"
        )
        _fail_silently = kwargs["fail_silently"] or False

        if not isinstance(_to, list):
            log.info("Destination address is not a list. Coercing to list.")
            _to = list(_to.split(","))

        clients_communication_history = ClientCommunication.objects.filter(
            Q(last_date_email__lte=three_months_ago)
            | Q(last_date_sms__lte=three_months_ago)
            | Q(last_date_call__lte=three_months_ago)
            | Q(last_date_face_to_face__lte=three_months_ago)
        )

        advisors = AdvisorContactDetail.objects.all()
        massMail = []
        body = ""
        to = []

        for advisor in advisors:
            advisor_clients_history = clients_communication_history.filter(
                client__advisor_id_fk=advisor.id
            )
            for client_history in advisor_clients_history:
                if client_history is not None:
                    body += (
                        "Name: "
                        + client_history.client.names
                        + " Surname: "
                        + client_history.client.surnames
                        + " Email: "
                        + client_history.client.client_contact_fk.email_address
                        + "\n"
                    )
            if body != "":
                to.append(advisor.email_address)
                massMail.append((_subject, body, _from, to))
                body = ""
            to = []

        massMail.append((_subject, _body, _from, _to),)

        send_mass_mail(tuple(massMail), _fail_silently)

    except Exception as e:
        log.error(f"Failed to send mail. Error: {e}")
        raise e
