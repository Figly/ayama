from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import construct_instance
from django.http.response import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from formtools.wizard.views import SessionWizardView

from . import models
from .forms import (AddClientContactDetailForm, AddClientDependentDetailsForm,
                    AddClientDetailForm, AddClientEmploymentetailForm,
                    AddClientRatesAndReturnForm)
from .models import (ClientContactDetail, ClientDetail, EmploymentDetail,
                     RatesAndReturn)

FORMS =[('0', AddClientDetailForm),
        ('1', AddClientContactDetailForm),
        ('2', AddClientEmploymentetailForm),
        ('3', AddClientRatesAndReturnForm),]

TEMPLATES = {"0":"clients/add_client_detail.html",
        "1":"clients/add_client_contact_detail.html",
        "2":"clients/add_client_employment_detail.html",
        "3":"clients/add_client_rates_detail.html"}

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

    def done(self, form_list, form_dict,**kwargs):
        #models backing db
        client = ClientDetail()
        contactDetail = ClientContactDetail()
        employmentDetail = EmploymentDetail()
        rates = RatesAndReturn()

        #form instances            
        client = construct_instance(form_dict["0"], client, form_dict["0"]._meta.fields, form_dict["0"]._meta.exclude)
        client.save()

        contactDetail = construct_instance(form_dict["1"], contactDetail, form_dict["1"]._meta.fields, form_dict["1"]._meta.exclude)
        contactDetail.client_id_fk = client
        contactDetail.save()

        employmentDetail = construct_instance(form_dict["2"], employmentDetail, form_dict["2"]._meta.fields, form_dict["2"]._meta.exclude)
        employmentDetail.client_id_fk = client
        employmentDetail.save()

        rates = construct_instance(form_dict["3"], rates, form_dict["3"]._meta.fields, form_dict["3"]._meta.exclude)
        rates.client_id_fk = client
        rates.save()
        messages.add_message(self.request, messages.SUCCESS, 'client successfully added.')
        return HttpResponseRedirect(reverse_lazy("home"))

class AddClientDependentView(LoginRequiredMixin, generic.CreateView):
    template_name = "clients/add_client_dependent_detail.html"
    form_class = AddClientDependentDetailsForm
    model = models.Dependent

    def form_valid(self, form):
        model = form.save(commit=False)
        messages.add_message(self.request, messages.SUCCESS, 'dependent successfully added.')
        if 'add-another' in self.request.POST:
            self.success_url = reverse_lazy("clients:add-client-dependents")
        elif 'submit' in self.request.POST:
            self.success_url = reverse_lazy("home")
        return super(AddClientDependentView, self).form_valid(form)
