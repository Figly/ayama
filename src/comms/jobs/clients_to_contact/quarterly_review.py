"""
Sample email send invocation using the Django email backend setup (hooked up to Sendgrid)
"""
import logging
from datetime import datetime, timedelta

import django
from django.core.mail import send_mass_mail
from django.db.models import Q

from clients.models.client_communication import ClientCommunication

log = logging.getLogger(__name__)


def run(**kwargs):
    django.setup()
    try:
        today = datetime.today()
        three_months_ago = today - timedelta(days=3)

        _subject = kwargs.get("subject", "No Subject")  # noqa
        _body = kwargs.get("body", "No body provided.")  # noqa
        _from = kwargs.get("from", "from@example.com")  # noqa
        _to = kwargs.get("to", "to@example.com")  # noqa
        _fail_silently = kwargs.get("fail_silently", False)  # noqa

        if not isinstance(_to, list):
            log.info("Destination address is not a list. Coercing to list.")
            _to = list(_to.split(","))

        datatuple = (
            (
                "Communication Reminder",
                "Communication reminder job run.",
                "karelverhoeven@gmail.com",
                [
                    "kylebrandin@gmail.com, karelverhoeven@gmail.com, coetzee.vs@gmail.com"
                ],
            ),
        )

        clients_late_communication = ClientCommunication.objects.filter(
            Q(last_date_email=three_months_ago)
            | Q(last_date_sms=three_months_ago)
            | Q(last_date_call=three_months_ago)
            | Q(last_date_face_to_face=three_months_ago)
        )

        # TODO: debug from here >> script runs fine up to this point
        # TODO: client_detail__advisor_id_fk >> not found in my linter - giving ref error
        # TODO: doesn't look like .insert is an identified method to extend tuples in Python > couldn't find anything,
        #       linter flagging issue
        # TODO: no email address found in message object
        # TODO: remove # noqa from script once everything is ready
        advisors_to_mail = clients_late_communication.filter(
            client_detail__advisor_id_fk  # noqa
        ).distinct(
            "id"
        )  # noqa

        message = ""
        for advisor in advisors_to_mail:
            message += clients_late_communication.filter(
                client_detail__advisor_id_fk=advisor.id
            ).only("names", "surnames", "client_contact_fk__email_address")
            datatuple.insert(
                (
                    "Communication Reminder",
                    message,
                    "karelverhoeven@gmail.com",
                    [message.email_address],
                )
            )

        send_mass_mail(datatuple)
    except Exception as e:
        log.error(f"Failed to send mail. Error: {e}")
        raise e
