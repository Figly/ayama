from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms.models import construct_instance
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from formtools.wizard.views import SessionWizardView

from ..forms import AddAdministratorContactDetailForm, AddAdministratorDetailForm
from ..models import AdministratorContactDetail, AdministratorDetail

FORMS = [
    ("0", AddAdministratorDetailForm),
    ("1", AddAdministratorContactDetailForm),
]

TEMPLATES = {
    "0": "practises/add_administrator.html",
    "1": "practises/add_administrator_contact_detail.html",
}


class AdministratorWizard(LoginRequiredMixin, UserPassesTestMixin, SessionWizardView):
    def test_func(self):
        return self.request.user.is_superuser

    def get_template_names(self):
        return TEMPLATES[self.steps.current]

    def get_context_data(self, form, **kwargs):
        context = super(AdministratorWizard, self).get_context_data(form=form, **kwargs)
        if self.steps.current != "0":
            administrator_name = []
            step0data = self.get_cleaned_data_for_step("0")
            administrator_name.append(step0data["title"].capitalize())
            administrator_name.append(step0data["initials"].capitalize())
            administrator_name.append(step0data["surnames"].capitalize())
            context.update({"administrator_name": " ".join(administrator_name)})
        return context

    def done(self, form_list, form_dict, **kwargs):
        # models backing db
        administrator = AdministratorDetail()
        administratorContactDetail = AdministratorContactDetail()
        User = get_user_model()

        # form instances
        administrator = construct_instance(
            form_dict["0"],
            administrator,
            form_dict["0"]._meta.fields,
            form_dict["0"]._meta.exclude,
        )

        administratorContactDetail = construct_instance(
            form_dict["1"],
            administratorContactDetail,
            form_dict["1"]._meta.fields,
            form_dict["1"]._meta.exclude,
        )

        User = User.objects.create_user(
            email=administratorContactDetail.email_address,
            username=administratorContactDetail.email_address,
            password="password",
            first_name=administrator.names,
            last_name=administrator.surnames,
            name=administrator.names + " " + administrator.surnames,
        )  # default password for now, to revise

        User.is_advisor = False
        User.is_administrator = True
        User.is_staff = True
        User.is_superuser = False
        User.save()
        administrator.user = User

        administratorContactDetail.modified_by = self.request.user
        administratorContactDetail.save()
        administrator.adminstrator_contact_fk = administratorContactDetail

        administrator.modified_by = self.request.user
        administrator.save()

        messages.add_message(
            self.request, messages.SUCCESS, "administrator successfully added."
        )

        return HttpResponseRedirect(reverse_lazy("home"))


class AministratorlistView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    template_name = "practises/administrator_list.html"
    model = AdministratorDetail

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super(AministratorlistView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_superuser:
            administrators = AdministratorDetail.objects.all().select_related(
                "adminstrator_contact_fk"
            )
            context = {"administrators": administrators}
        elif user.is_superuser:
            return HttpResponseRedirect(reverse_lazy("home"))

        return context


class AdministratorSummaryView(
    LoginRequiredMixin, UserPassesTestMixin, generic.DetailView
):
    template_name = "practises/administrator_summary.html"
    model = AdministratorDetail

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super(AdministratorSummaryView, self).get_context_data(**kwargs)
        administrator_id = self.kwargs["pk"]
        administrator = AdministratorDetail.objects.get(user=administrator_id)
        context = {"administrator": administrator}
        return context


class EditAdministratorDetailView(
    LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView
):
    template_name = "practises/edit_administrator_detail.html"
    model = AdministratorDetail
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
        return self.request.user.is_superuser

    def form_valid(self, form):
        if "cancel" in self.request.POST:
            url = reverse_lazy("home")
            return HttpResponseRedirect(url)

        model = form.save(commit=False)
        model.modified_by = self.request.user
        model.save

        messages.add_message(
            self.request, messages.SUCCESS, "administrator details successfully edited."
        )
        self.success_url = reverse_lazy("home")
        return super(EditAdministratorDetailView, self).form_valid(form)


class EditAdministratorContactView(
    LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView
):
    template_name = "practises/edit_administrator_detail.html"
    model = AdministratorContactDetail
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
        return self.request.user.is_superuser

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
            "administrator contact details successfully edited.",
        )
        self.success_url = reverse_lazy("home")
        return super(EditAdministratorContactView, self).form_valid(form)
