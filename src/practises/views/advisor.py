from __future__ import unicode_literals

import logging

from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.db import transaction
from django.db.models.query_utils import Q
from django.forms.models import construct_instance
from django.http import JsonResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic
from formtools.wizard.views import SessionWizardView

from ..filters import AdvisorFilter
from ..forms import AddAdvisorContactDetailForm, AddAdvisorDetailForm
from ..models import (
    AdministratorDetail,
    AdvisorContactDetail,
    AdvisorDetail,
    AdvisorReminderConfig,
    PractiseDetail,
    User,
)

FORMS = [
    ("0", AddAdvisorDetailForm),
    ("1", AddAdvisorContactDetailForm),
]

TEMPLATES = {
    "0": "practises/add_advisor_detail.html",
    "1": "practises/add_advisor_contact_detail.html",
}

log = logging.getLogger(__name__)


class AddAdvisorWizard(LoginRequiredMixin, UserPassesTestMixin, SessionWizardView):
    def test_func(self):
        return self.request.user.is_administrator or self.request.user.is_superuser

    def get_template_names(self):
        return TEMPLATES[self.steps.current]

    def dispatch(self, request, *args, **kwargs):
        self.practise = kwargs.get("practise", None)
        return super(AddAdvisorWizard, self).dispatch(request, *args, **kwargs)

    def get_form(self, step=None, data=None, files=None):
        form = super().get_form(step, data, files)
        if self.steps.current == "0" and step is None:
            if self.request.user.is_superuser:
                form.fields["practise_id_fk"].queryset = PractiseDetail.objects.all()
            elif self.request.user.is_administrator and self.request.user.is_advisor:
                practise_id = self.request.user.Advisor.practise_id_fk.id
                form.fields["practise_id_fk"].queryset = PractiseDetail.objects.filter(
                    id=practise_id
                ).all()
            elif self.request.user.is_administrator:
                practise_id = self.request.user.Administrator.practise_id_fk.id
                form.fields["practise_id_fk"].queryset = PractiseDetail.objects.filter(
                    id=practise_id
                ).all()

        return form

    def get_form_initial(self, step):
        self.initial_dict.get(self.steps.current, {})
        if self.steps.current == "0" and self.practise is not None:
            return self.initial_dict.get(step, {"practise_id_fk": self.practise})
        elif self.request.user.is_administrator and self.request.user.is_advisor:
            self.practise = self.request.user.Advisor.practise_id_fk
            return self.initial_dict.get(step, {"practise_id_fk": self.practise})
        elif self.request.user.is_administrator:
            self.practise = self.request.user.Administrator.practise_id_fk
            return self.initial_dict.get(step, {"practise_id_fk": self.practise})

    def get_context_data(self, form, **kwargs):
        context = super(AddAdvisorWizard, self).get_context_data(form=form, **kwargs)
        if self.steps.current != "0":
            advisor_name = []
            step0data = self.get_cleaned_data_for_step("0")
            advisor_name.append(step0data["title"].capitalize())
            advisor_name.append(step0data["initials"].capitalize())
            advisor_name.append(step0data["surnames"].capitalize())
            context.update({"advisor_name": " ".join(advisor_name)})
        return context

    @transaction.atomic
    def done(self, form_list, form_dict, **kwargs):
        try:
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

            existing_user = User.objects.filter(
                Q(email=advisorContact.email_address)
                | Q(username=advisorContact.email_address)
            )

            if not existing_user:
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
                user.save()
                advisor.user = user

                advisorContact.modified_by = self.request.user
                advisorContact.save()
                advisor.advisor_contact_fk = advisorContact

                advisorCommsConfig.modified_by = self.request.user
                advisorCommsConfig.save()

                advisor.reminder_config_freq_fk = advisorCommsConfig
                advisor.modified_by = self.request.user

                advisor.save()

                messages.add_message(
                    self.request, messages.SUCCESS, "advisor successfully added."
                )
            else:
                messages.add_message(
                    self.request, messages.ERROR, "Email address already in use."
                )
                return HttpResponseRedirect(self.request.path_info)
        except Exception as e:
            log.info(e)
            messages.add_message(
                self.request, messages.ERROR, "An error occured. Please try again."
            )
            return HttpResponseRedirect(reverse_lazy("home"))

        return HttpResponseRedirect(reverse_lazy("home"))


class AdvisorlistView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    template_name = "practises/advisor_list.html"
    model = AdvisorDetail

    def test_func(self):
        return self.request.user.is_administrator or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super(AdvisorlistView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_administrator and user.is_advisor:
            advisors = AdvisorDetail.objects.filter(
                practise_id_fk=user.Advisor.practise_id_fk
            ).select_related("advisor_contact_fk")
            context = {"advisors": advisors}
        elif user.is_administrator:
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
        "residential_suburb",
        "residential_city",
        "residential_country",
        "residential_code",
        "postal_address_line_1",
        "postal_address_line_2",
        "postal_suburb",
        "postal_city",
        "postal_country",
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


def AdvisorSearch(request):
    advisor_list = AdvisorDetail.objects.filter(practise_id_fk=None)
    advisor_filter = AdvisorFilter(request.GET, queryset=advisor_list)
    return render(request, "practises/advisor_search.html", {"filter": advisor_filter})


class InviteAdvisor(generic.View):
    def post(self, request, *args, **kwargs):
        try:
            advisor_id = request.POST.get("advisor_id", None)
            admin_id = request.POST.get("admin_id")

            if advisor_id is None or admin_id is None:
                return JsonResponse({"valid": False}, status=400)

            advisor = get_object_or_404(AdvisorDetail, pk=advisor_id)
            admin = get_object_or_404(AdministratorDetail, pk=admin_id)
            practise = get_object_or_404(PractiseDetail, pk=admin.practise_id_fk.id)

            # current_site = Site.objects.get_current()
            # current_site.domain

            # TODO:replace https below with the above
            link = (
                "https://www.figly.io/link_advisor?advisorid="
                + advisor_id
                + "&practiseid="
                + str(admin.practise_id_fk.id)
            )

            send_mail(
                practise.name + " invited you to join their practise.",
                "Click: " + link,
                "karelverhoeven@gmail.com",
                [advisor.advisor_contact_fk.email_address],
                fail_silently=False,
            )

            return JsonResponse({"valid": True}, status=200)
        except Exception as e:
            log.info(e)
            return JsonResponse(
                {"valid": "An error occured. Please contact an administrator"},
                status=400,
            )


class LinkAdvisor(generic.View):
    def get(self, request, *args, **kwargs):
        try:
            advisor_id = request.GET["advisorid"]
            practise_id = request.GET["practiseid"]

            advisor = get_object_or_404(AdvisorDetail, pk=advisor_id)
            practise = get_object_or_404(PractiseDetail, pk=practise_id)

            if advisor.practise_id_fk is not None:
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    "Advisor is already associated with a practise.",
                )
                url = reverse_lazy("home")
                return HttpResponseRedirect(url)

            advisor.practise_id_fk = practise
            advisor.save()

            messages.add_message(
                self.request,
                messages.SUCCESS,
                "You have succesfully been linked to a practise.",
            )

            url = reverse_lazy("home")
            return HttpResponseRedirect(url)
        except Exception as e:
            log.info(e)
            messages.add_message(
                self.request,
                messages.ERROR,
                "An error occured. Please contact an administrator.",
            )
            url = reverse_lazy("home")
            return HttpResponseRedirect(url)


class EditRolesView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    template_name = "practises/edit_advisor_detail.html"

    model = User
    fields = (
        "is_administrator",
        "is_advisor",
    )
    widgets = {
        "is_administrator": forms.CheckboxInput(),
        "is_advisor": forms.CheckboxInput(),
    }

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
            self.request, messages.SUCCESS, "advisor roles successfully edited.",
        )
        self.success_url = reverse_lazy("home")
        return super(EditRolesView, self).form_valid(form)
