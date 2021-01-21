from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import construct_instance
from django.http.response import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from formtools.wizard.views import SessionWizardView
from practises.models import AdvisorDetail, AdvisorReminderConfig

from ..forms import (
    AddClientContactDetailForm,
    AddClientDetailForm,
    AddClientEmploymentDetailForm,
    AddClientRatesAndReturnForm,
)
from ..models import (
    ClientCommunication,
    ClientCommunicationFrequency,
    ClientContactDetail,
    ClientDetail,
    EmploymentDetail,
    RatesAndReturn,
)

FORMS = [
    ("0", AddClientDetailForm),
    ("1", AddClientContactDetailForm),
    ("2", AddClientEmploymentDetailForm),
    ("3", AddClientRatesAndReturnForm),
]

TEMPLATES = {
    "0": "clients/add_client_detail.html",
    "1": "clients/add_client_contact_detail.html",
    "2": "clients/add_client_employment_detail.html",
    "3": "clients/add_client_rates_detail.html",
}


class ClientWizard(LoginRequiredMixin, SessionWizardView):
    def get_template_names(self):
        return TEMPLATES[self.steps.current]

    def get_form(self, step=None, data=None, files=None):
        form = super(ClientWizard, self).get_form(step, data, files)
        user = self.request.user

        if self.steps.current == "0" and step is None:
            if user.is_administrator and user.is_advisor:
                practise_id = user.Advisor.practise_id_fk
                form.fields["advisor_id_fk"].queryset = AdvisorDetail.objects.filter(
                    practise_id_fk=practise_id
                )
            elif user.is_administrator:
                practise_id = user.Administrator.practise_id_fk
                form.fields["advisor_id_fk"].queryset = AdvisorDetail.objects.filter(
                    practise_id_fk=practise_id
                )
            elif user.is_advisor:
                advisor_id = user.id
                form.fields["advisor_id_fk"].queryset = AdvisorDetail.objects.filter(
                    user_id=advisor_id
                )

        return form

    def get_context_data(self, form, **kwargs):
        user = self.request.user  # noqa
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
        clientComm = ClientCommunication()
        communicationFrequency = ClientCommunicationFrequency()

        # form instances
        contactDetail = construct_instance(
            form_dict["1"],
            contactDetail,
            form_dict["1"]._meta.fields,
            form_dict["1"]._meta.exclude,
        )
        contactDetail.modified_by = self.request.user
        contactDetail.save()

        employmentDetail = construct_instance(
            form_dict["2"],
            employmentDetail,
            form_dict["2"]._meta.fields,
            form_dict["2"]._meta.exclude,
        )
        employmentDetail.modified_by = self.request.user
        employmentDetail.save()

        rates = construct_instance(
            form_dict["3"],
            rates,
            form_dict["3"]._meta.fields,
            form_dict["3"]._meta.exclude,
        )
        rates.modified_by = self.request.user
        rates.save()

        client = construct_instance(
            form_dict["0"],
            client,
            form_dict["0"]._meta.fields,
            form_dict["0"]._meta.exclude,
        )

        clientComm.modified_by = self.request.user
        clientComm.save()
        client.client_comms_fk = clientComm

        advisorConfig = client.advisor_id_fk.reminder_config_freq_fk

        communicationFrequency.sms_frequency = advisorConfig.sms_frequency
        communicationFrequency.face_to_face_frequency = (
            advisorConfig.face_to_face_frequency
        )
        communicationFrequency.calls_frequency = advisorConfig.calls_frequency
        communicationFrequency.email_frequency = advisorConfig.email_frequency
        communicationFrequency.modified_by = self.request.user
        communicationFrequency.save()

        client.client_comms_freq_fk = communicationFrequency
        client.client_contact_fk = contactDetail
        client.client_employment_fk = employmentDetail
        client.client_rates_fk = rates
        client.modified_by = self.request.user
        client.save()

        messages.add_message(
            self.request, messages.SUCCESS, "client successfully added."
        )
        return HttpResponseRedirect(reverse_lazy("home"))


class ClientlistView(LoginRequiredMixin, generic.ListView):
    template_name = "clients/client_list.html"
    model = ClientDetail

    def get_context_data(self, **kwargs):
        context = super(ClientlistView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_superuser:
            clients = ClientDetail.objects.all().select_related("client_contact_fk")
        elif user.is_administrator:
            practise_id = user.Administrator.practise_id_fk
            advisors = AdvisorDetail.objects.filter(practise_id_fk=practise_id)
            clients = ClientDetail.objects.filter(
                advisor_id_fk__in=advisors
            ).select_related("client_contact_fk")
        elif user.is_advisor:
            clients = ClientDetail.objects.filter(advisor_id_fk=user.id).select_related(
                "client_contact_fk"
            )

        context = {"clients": clients}
        return context

class AdvisorClientsView(LoginRequiredMixin, generic.ListView):
    template_name = "clients/advisor_clients.html"
    model = ClientDetail

    def get_context_data(self, **kwargs):
        context = super(AdvisorClientsView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_superuser:
            clients = ClientDetail.objects.all().select_related("client_contact_fk")
        elif user.is_administrator:
            practise_id = user.Administrator.practise_id_fk
            advisors = AdvisorDetail.objects.filter(practise_id_fk=practise_id)
            clients = ClientDetail.objects.filter(
                advisor_id_fk__in=advisors
            ).select_related("client_contact_fk")
        elif user.is_advisor:
            clients = ClientDetail.objects.filter(advisor_id_fk=user.id).select_related(
                "client_contact_fk"
            )

        context = {"clients": clients}
        return context


class ClientSummaryView(LoginRequiredMixin, generic.DetailView):
    template_name = "clients/client_summary.html"
    model = ClientDetail

    def get_context_data(self, **kwargs):
        context = super(ClientSummaryView, self).get_context_data(**kwargs)
        client_id = self.kwargs["pk"]
        client = ClientDetail.objects.get(id=client_id)

        context = {"client": client}
        return context


class EditClientDetailsView(LoginRequiredMixin, generic.UpdateView):
    template_name = "clients/edit_details.html"
    model = ClientDetail
    fields = (
        "title",
        "initials",
        "surnames",
        "names",
        "known_as",
        "sa_id",
        "passport_no",
    )

    def form_valid(self, form):
        if "cancel" in self.request.POST:
            url = reverse_lazy("home")
            return HttpResponseRedirect(url)

        model = form.save(commit=False)
        model.modified_by = self.request.user
        model.save

        messages.add_message(
            self.request, messages.SUCCESS, "client details successfully edited."
        )
        self.success_url = reverse_lazy("home")
        return super(EditClientDetailsView, self).form_valid(form)


class EditClientContactView(LoginRequiredMixin, generic.UpdateView):
    template_name = "clients/edit_details.html"
    model = ClientContactDetail
    fields = (
        "telephone_home",
        "telephone_work",
        "cellphone_number",
        "fax_number",
        "email_address",
        "residential_address_line_1",
        "residential_address_line_2",
        "residential_code",
        "postal_address_line_1",
        "postal_address_line_2",
        "postal_code",
    )

    def form_valid(self, form):
        if "cancel" in self.request.POST:
            url = reverse_lazy("home")
            return HttpResponseRedirect(url)

        model = form.save(commit=False)
        model.modified_by = self.request.user
        model.save

        messages.add_message(
            self.request,
            messages.SUCCESS,
            "client contact details successfully edited.",
        )
        self.success_url = reverse_lazy("home")
        return super(EditClientContactView, self).form_valid(form)


class EditClientEmploymentView(LoginRequiredMixin, generic.UpdateView):
    template_name = "clients/edit_details.html"
    model = EmploymentDetail
    fields = (
        "company_name",
        "occupation",
        "employment_date",
        "personnel_number",
        "medical_aid",
        "retirement_fund_current_value",
        "group_life_cover",
    )

    def form_valid(self, form):
        if "cancel" in self.request.POST:
            url = reverse_lazy("home")
            return HttpResponseRedirect(url)

        model = form.save(commit=False)
        model.modified_by = self.request.user
        model.save

        messages.add_message(
            self.request,
            messages.SUCCESS,
            "client employment details successfully edited.",
        )
        self.success_url = reverse_lazy("home")
        return super(EditClientEmploymentView, self).form_valid(form)


class EditClientRatesView(LoginRequiredMixin, generic.UpdateView):
    template_name = "clients/edit_details.html"
    model = RatesAndReturn
    fields = (
        "inflation",
        "interest",
        "return_rate",
    )

    def form_valid(self, form):
        if "cancel" in self.request.POST:
            url = reverse_lazy("home")
            return HttpResponseRedirect(url)

        model = form.save(commit=False)
        model.modified_by = self.request.user
        model.save

        messages.add_message(
            self.request,
            messages.SUCCESS,
            "client rates and return details successfully edited.",
        )
        self.success_url = reverse_lazy("home")
        return super(EditClientRatesView, self).form_valid(form)
