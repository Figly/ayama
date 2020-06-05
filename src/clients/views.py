from __future__ import unicode_literals

import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import construct_instance
from django.http.response import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from formtools.wizard.views import SessionWizardView

from practises.models import AdvisorDetail

from .forms import (AddClientContactDetailForm, AddClientDependentDetailsForm,
                    AddClientDetailForm, AddClientEmploymentetailForm,
                    AddClientRatesAndReturnForm)
from .models import (ClientContactDetail, ClientDetail, Dependent,
                     EmploymentDetail, RatesAndReturn)

FORMS = [
    ("0", AddClientDetailForm),
    ("1", AddClientContactDetailForm),
    ("2", AddClientEmploymentetailForm),
    ("3", AddClientRatesAndReturnForm),
]

TEMPLATES = {
    "0": "clients/add_client_detail.html",
    "1": "clients/add_client_contact_detail.html",
    "2": "clients/add_client_employment_detail.html",
    "3": "clients/add_client_rates_detail.html",
}


class ClientWizard(SessionWizardView):
    def get_template_names(self):
        return TEMPLATES[self.steps.current]

    def get_context_data(self, form, **kwargs):
        context = super(ClientWizard, self).get_context_data(form=form, **kwargs)
        if self.steps.current != "0":
            client_name = []
            step0data = self.get_cleaned_data_for_step("0")
            client_name.append(step0data["title"].capitalize())
            client_name.append(step0data["initials"].capitalize())
            client_name.append(step0data["surnames"].capitalize())
            context.update({"client_name": " ".join(client_name)})
        return context

    def done(self, form_list, form_dict, **kwargs):
        # models backing db
        client = ClientDetail()
        contactDetail = ClientContactDetail()
        employmentDetail = EmploymentDetail()
        rates = RatesAndReturn()

        # form instances
        contactDetail = construct_instance(
            form_dict["1"],
            contactDetail,
            form_dict["1"]._meta.fields,
            form_dict["1"]._meta.exclude,
        )
        contactDetail.save()

        employmentDetail = construct_instance(
            form_dict["2"],
            employmentDetail,
            form_dict["2"]._meta.fields,
            form_dict["2"]._meta.exclude,
        )
        employmentDetail.save()

        rates = construct_instance(
            form_dict["3"],
            rates,
            form_dict["3"]._meta.fields,
            form_dict["3"]._meta.exclude,
        )
        rates.save()

        client = construct_instance(
            form_dict["0"],
            client,
            form_dict["0"]._meta.fields,
            form_dict["0"]._meta.exclude,
        )

        client.client_contact_fk = contactDetail
        client.client_employment_fk = employmentDetail
        client.client_rates_fk = rates
        client.save()

        messages.add_message(
            self.request, messages.SUCCESS, "client successfully added."
        )
        return HttpResponseRedirect(reverse_lazy("home"))


class AddClientDependentView(LoginRequiredMixin, generic.CreateView):
    template_name = "clients/add_client_dependent_detail.html"
    form_class = AddClientDependentDetailsForm
    model = Dependent

    def form_valid(self, form):
        model = form.save(commit=False)  # noqa
        messages.add_message(
            self.request, messages.SUCCESS, "dependent successfully added."
        )
        if "add-another" in self.request.POST:
            self.success_url = reverse_lazy("clients:add-client-dependents")
        elif "submit" in self.request.POST:
            self.success_url = reverse_lazy("home")
        return super(AddClientDependentView, self).form_valid(form)

class ClientlistView(generic.ListView):
    template_name = "clients/client_list.html"
    model = ClientDetail

    def get_context_data(self, **kwargs):
        context = super(ClientlistView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_superuser:
            clients = ClientDetail.objects.all().select_related('client_contact_fk')
        elif user.is_administrator:
            practise_id = user.AdministratorDetail.practise_id_fk
            advisors = AdvisorDetail.objects.filter(practise_id_fk= practise_id)
            clients = ClientDetail.objects.filter(advisor_id_fk__in = advisors).select_related('client_contact_fk')
        elif user.is_advisor:
            clients = ClientDetail.objects.all(advisor_id_fk = user.AdvisorDetail).select_related('client_contact_fk')

        context = {'clients':clients}
        return context

class ClientSummaryView(generic.DetailView):
    template_name = "clients/client_summary.html"
    model = ClientDetail

    def get_context_data(self, **kwargs):
        context = super(ClientSummaryView, self).get_context_data(**kwargs)
        client_id = self.kwargs["pk"]
        client = ClientDetail.objects.get(id = client_id)

        context = {'client':client}
        return context
