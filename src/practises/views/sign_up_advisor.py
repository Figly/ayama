from __future__ import unicode_literals

import logging

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.db.models.query_utils import Q
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
log = logging.getLogger(__name__)


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
                    self.request, messages.SUCCESS, "Advisor successfully signed up."
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
