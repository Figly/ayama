from __future__ import unicode_literals

import logging

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Q
from django.forms.models import construct_instance
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from formtools.wizard.views import SessionWizardView

from ..forms import (
    AddAdministratorContactDetailForm,
    AddPractiseDetailForm,
    SignUpAdministratorDetailForm,
)
from ..models import AdministratorContactDetail, AdministratorDetail, PractiseDetail

FORMS = [
    ("0", SignUpAdministratorDetailForm),
    ("1", AddAdministratorContactDetailForm),
    ("2", AddPractiseDetailForm),
]

TEMPLATES = {
    "0": "practises/add_administrator.html",
    "1": "practises/signup_administrator_contact_detail.html",
    "2": "practises/signup_practise_detail.html",
}
log = logging.getLogger(__name__)


class SignUpAdministratorWizard(SessionWizardView):
    def test_func(self):
        return self.request.user.is_superuser

    def get_template_names(self):
        return TEMPLATES[self.steps.current]

    def get_context_data(self, form, **kwargs):
        context = super(SignUpAdministratorWizard, self).get_context_data(
            form=form, **kwargs
        )

        if self.steps.current != "0":
            administrator_name = []
            step0data = self.get_cleaned_data_for_step("0")
            administrator_name.append(step0data["title"].capitalize())
            administrator_name.append(step0data["initials"].capitalize())
            administrator_name.append(step0data["surnames"].capitalize())
            context.update({"administrator_name": " ".join(administrator_name)})

        return context

    @transaction.atomic
    def done(self, form_list, form_dict, **kwargs):
        try:
            # models backing db
            practise = PractiseDetail()
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

            practise = construct_instance(
                form_dict["2"],
                practise,
                form_dict["2"]._meta.fields,
                form_dict["2"]._meta.exclude,
            )

            existing_user = User.objects.filter(
                Q(email=administratorContactDetail.email_address)
                | Q(username=administratorContactDetail.email_address)
            )

            if not existing_user:

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
                User.is_active = False  # user set to inactive until email verification
                User.save()
                administrator.user = User

                practise.modified_by = administrator.user
                practise.save()
                administrator.practise_id_fk = practise

                administratorContactDetail.modified_by = administrator.user
                administratorContactDetail.save()
                administrator.adminstrator_contact_fk = administratorContactDetail

                administrator.modified_by = administrator.user
                administrator.save()

                link = "{0}://{1}{2}".format(
                    self.request.scheme, self.request.get_host(), "/password-reset"
                )

                send_mail(
                    "Complete registration below",
                    "Click: " + link + " to set up a new password.",
                    "karelverhoeven@gmail.com",
                    [administratorContactDetail.email_address],
                    fail_silently=False,
                )

                messages.add_message(
                    self.request,
                    messages.SUCCESS,
                    "Practise and Administrator successfully signed up.",
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
