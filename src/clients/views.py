from __future__ import unicode_literals

from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AddClientDetailForm, AddClientContactDetailForm, AddClientEmploymentetailForm, AddClientRatesAndReturnForm, AddClientDependentDetailsForm
from . import models
from formtools.wizard.views import SessionWizardView
from django.http.response import HttpResponseRedirect

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

    def done(self, form_list, **kwargs):
        return HttpResponseRedirect(reverse_lazy("home"))
