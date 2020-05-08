from __future__ import unicode_literals

from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AddClientDetailForm, AddClientContactDetailForm, AddClientEmploymentetailForm, AddClientRatesAndReturnForm, AddClientDependentDetailsForm
from . import models
from formtools.wizard.views import SessionWizardView
from django.http.response import HttpResponseRedirect
import logging

FORMS =[('0', AddClientDetailForm),
        ('1', AddClientContactDetailForm),
        ('2', AddClientEmploymentetailForm),
        ('3', AddClientRatesAndReturnForm),
        ('4', AddClientDependentDetailsForm),]

TEMPLATES = {"0":"clients/add_client_detail.html",
        "1":"clients/add_client_contact_detail.html",
        "2":"clients/add_client_employment_detail.html",
        "3":"clients/add_client_rates_detail.html",
        "4":"clients/add_client_dependent_detail.html"}

class ClientWizard(SessionWizardView):
    def get_template_names(self):
        return TEMPLATES[self.steps.current]

    def get_context_data(self, form, **kwargs):
        context = super(ClientWizard, self).get_context_data(form=form, **kwargs)
        if self.steps.current != '0':
            client_name = []
            step0data = self.get_cleaned_data_for_step('0')
            client_name.append(step0data["title"].capitalize())
            client_name.append(step0data["initials"].capitalize())
            client_name.append(step0data["surnames"].capitalize())
            context.update({'client_name':' '.join(client_name)})
        return context

    def done(self, form_list, **kwargs):
        # client = form_list[0].cleaned_data['names']
        # logger = logging.getLogger("django")
        # logger.info(client)

        return HttpResponseRedirect(reverse_lazy("home"))
