from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms.models import construct_instance
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from formtools.wizard.views import SessionWizardView

from ..forms import AddAdvisorContactDetailForm, SignUpAdvisorDetailForm
from ..models import (
    AdministratorDetail,
    AdvisorContactDetail,
    AdvisorDetail,
    AdvisorReminderConfig,
    PractiseDetail,
)

FORMS = [
    ("0", SignUpAdvisorDetailForm),
    ("1", AddAdvisorContactDetailForm),
]

TEMPLATES = {
    "0": "practises/add_advisor_detail.html",
    "1": "practises/add_advisor_contact_detail.html",
}


class SignUpAdvisorWizard(SessionWizardView):
    def test_func(self):
        return self.request.user.is_administrator or self.request.user.is_superuser

    def get_template_names(self):
        return TEMPLATES[self.steps.current]

    def dispatch(self, request, *args, **kwargs):
        self.practise = kwargs.get("practise", None)
        return super(SignUpAdvisorWizard, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, form, **kwargs):
        context = super(SignUpAdvisorWizard, self).get_context_data(form=form, **kwargs)
        if self.steps.current != "0":
            advisor_name = []
            step0data = self.get_cleaned_data_for_step("0")
            advisor_name.append(step0data["title"].capitalize())
            advisor_name.append(step0data["initials"].capitalize())
            advisor_name.append(step0data["surnames"].capitalize())
            context.update({"advisor_name": " ".join(advisor_name)})
        return context

    def done(self, form_list, form_dict, **kwargs):
        User = get_user_model()
        # models backing db
        advisor = AdvisorDetail()
        advisorContact = AdvisorContactDetail()
        advisorCommsConfig = AdvisorReminderConfig()

        # form instances

        advisor = construct_instance(
            form_dict["0"],
            advisor,
            form_dict["0"]._meta.fields,
            form_dict["0"]._meta.exclude,
        )

        advisorContact = construct_instance(
            form_dict["1"],
            advisorContact,
            form_dict["1"]._meta.fields,
            form_dict["1"]._meta.exclude,
        )

        user = User.objects.create_user(
            email=advisorContact.email_address,
            username=advisorContact.email_address,
            password="password",
            first_name=advisor.names,
            last_name=advisor.surnames,
            name=advisor.names + " " + advisor.surnames,
        )  # default password for now, to revise
        user.is_advisor = True
        user.is_administrator = False
        user.is_staff = True
        user.is_superuser = False
        user.is_active = False  # add email registration
        user.save()
        advisor.user = user

        advisorContact.modified_by = advisor.user
        advisorContact.save()
        advisor.advisor_contact_fk = advisorContact

        advisorCommsConfig.modified_by = advisor.user
        advisorCommsConfig.save()

        advisor.reminder_config_freq_fk = advisorCommsConfig
        advisor.modified_by = advisor.user

        advisor.save()

        messages.add_message(
            self.request, messages.SUCCESS, "advisor successfully added."
        )

        return HttpResponseRedirect(reverse_lazy("home"))


class AdvisorlistView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    template_name = "practises/advisor_list.html"
    model = AdvisorDetail

    def test_func(self):
        return self.request.user.is_administrator or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super(AdvisorlistView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_administrator:
            advisors = AdvisorDetail.objects.filter(
                practise_id_fk=user.Administrator.practise_id_fk
            ).select_related("advisor_contact_fk")
            context = {"advisors": advisors}
        elif user.is_superuser:
            advisors = AdvisorDetail.objects.all().select_related("advisor_contact_fk")
            context = {"advisors": advisors}

        return context


class AdvisorSummaryView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    template_name = "practises/advisor_summary.html"
    model = AdvisorDetail

    def test_func(self):
        return self.request.user.is_administrator or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super(AdvisorSummaryView, self).get_context_data(**kwargs)
        advisor_id = self.kwargs["pk"]
        advisor = AdvisorDetail.objects.get(user=advisor_id)
        context = {"advisor": advisor}
        return context


class EditAdvisorDetailView(
    LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView
):
    template_name = "practises/edit_advisor_detail.html"
    model = AdvisorDetail
    fields = (
        "title",
        "initials",
        "surnames",
        "names",
        "known_as",
        "sa_id",
        "passport_no",
        "position",
        "employment_date",
        "personnel_number",
    )

    def test_func(self):
        return self.request.user.is_administrator or self.request.user.is_superuser

    def form_valid(self, form):
        if "cancel" in self.request.POST:
            url = reverse_lazy("home")
            return HttpResponseRedirect(url)

        model = form.save(commit=False)
        model.modified_by = self.request.user
        model.save

        messages.add_message(
            self.request, messages.SUCCESS, "advisor details successfully edited."
        )
        self.success_url = reverse_lazy("home")
        return super(EditAdvisorDetailView, self).form_valid(form)


class EditAdvisorContactView(
    LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView
):
    template_name = "practises/edit_advisor_detail.html"

    model = AdvisorContactDetail
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

    def test_func(self):
        return self.request.user.is_administrator or self.request.user.is_superuser

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
            "advisor contact details successfully edited.",
        )
        self.success_url = reverse_lazy("home")
        return super(EditAdvisorContactView, self).form_valid(form)


class EditReminderPreferencesView(
    LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView
):
    template_name = "practises/edit_advisor_detail.html"
    model = AdvisorReminderConfig
    fields = (
        "face_to_face_frequency",
        "calls_frequency",
        "email_frequency",
        "sms_frequency",
    )

    def test_func(self):
        return self.request.user.is_advisor

    def form_valid(self, form):
        if "cancel" in self.request.POST:
            url = reverse_lazy("home")
            return HttpResponseRedirect(url)

        model = form.save(commit=False)
        model.modified_by = self.request.user
        model.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            "communication frequency successfully edited.",
        )
        self.success_url = reverse_lazy("home")
        return super(EditReminderPreferencesView, self).form_valid(form)
