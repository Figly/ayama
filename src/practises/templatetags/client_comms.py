import datetime

from django import template
from django.db.models import DateField, ExpressionWrapper, F

from clients.models import ClientDetail

register = template.Library()

@register.inclusion_tag('practises/client_communications.html', takes_context=True)

def client_comms(context, id):
    
    dateUntil = datetime.datetime.now().date() + datetime.timedelta(weeks=4)

    client_comm_history = (ClientDetail.objects.filter(advisor_id_fk = id)
                            .select_related('client_comms_fk')
                            .select_related('client_comms_freq_fk')
                            .all())
    
    last_seen = client_comm_history.filter(client_comms_fk__last_date_face_to_face__lte = dateUntil).all().order_by('client_comms_fk__last_date_face_to_face')

    last_sms = client_comm_history.filter(client_comms_fk__last_date_sms__lte = dateUntil).all().order_by('client_comms_fk__last_date_sms')

    last_email = client_comm_history.filter(client_comms_fk__last_date_email__lte = dateUntil).all().order_by('client_comms_fk__last_date_email')

    last_call = client_comm_history.filter(client_comms_fk__last_date_call__lte = dateUntil).all().order_by('client_comms_fk__last_date_call')   
    return {
        'last_seen': last_seen,
        'last_sms':last_sms,
        'last_email': last_email,
        'last_call':last_call
        }
