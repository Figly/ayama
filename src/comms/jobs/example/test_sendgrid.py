"""
Sample email send invocation using the Django email backend setup (hooked up to Sendgrid)
"""
import logging

from django.core.mail import send_mail

log = logging.getLogger(__name__)


def run(**kwargs):
    try:
        _subject = kwargs.get("subject", "No Subject")
        _body = kwargs.get("body", "No body provided.")
        _from = kwargs.get("from", "from@example.com")
        _to = kwargs.get("to", "to@example.com")
        _fail_silently = kwargs.get("fail_silently", False)

        if not isinstance(_to, list):
            log.info("Destination address is not a list. Coercing to list.")
            _to = list(_to.split(","))

        send_mail(
            _subject, _body, _from, _to, fail_silently=_fail_silently,
        )
    except Exception as e:
        log.error(f"Failed to send mail. Error: {e}")
        raise e


# TODO
# Sender Authentication
# We can also make some improvements, like
# Domain Authentication at https://app.sendgrid.com/settings/sender_auth to
# improve deliverability by proving to inbox providers that you own the domain you’re sending from.
#
# Send emails from own domain
# Also, instead of sending emails from accounts like &mldr@sendgrid.net,
# it would be better to have them with our domain &mldr@mydomain.com.
# In SendGrid this is called Link Branding and can be configured at:
# https://app.sendgrid.com/settings/sender_auth/link/create
