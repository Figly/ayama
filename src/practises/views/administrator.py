from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import construct_instance
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from formtools.wizard.views import SessionWizardView

from ..forms import (AddAdministratorContactDetailForm,
                     AddAdministratorDetailForm)
from ..models import AdministratorContactDetail, AdministratorDetail

FORMS =[('0', AddAdministratorDetailForm),
        ('1', AddAdministratorContactDetailForm),]

TEMPLATES = {"0":"practises/add_administrator.html",
        "1":"practises/add_administrator_contact_detail.html"}

class AdministratorWizard(SessionWizardView):
    def get_template_names(self):
        return TEMPLATES[self.steps.current]

    def get_context_data(self, form, **kwargs):
        context = super(AdministratorWizard, self).get_context_data(form=form, **kwargs)
        if self.steps.current != '0':
            administrator_name = []
            step0data = self.get_cleaned_data_for_step('0')
            administrator_name.append(step0data["title"].capitalize())
            administrator_name.append(step0data["initials"].capitalize())
            administrator_name.append(step0data["surnames"].capitalize())
            context.update({'administrator_name':' '.join(administrator_name)})
        return context

    def done(self, form_list, form_dict,**kwargs):
                #models backing db
        administrator = AdministratorDetail()
        administratorContactDetail = AdministratorContactDetail()

        #form instances            
        administrator = construct_instance(form_dict["0"], administrator, form_dict["0"]._meta.fields, form_dict["0"]._meta.exclude)
        administrator.save()

        administratorContactDetail = construct_instance(form_dict["1"], administratorContactDetail, form_dict["1"]._meta.fields, form_dict["1"]._meta.exclude)
        administratorContactDetail.adminstrator_id_fk = administrator
        administratorContactDetail.save()

        messages.add_message(self.request, messages.SUCCESS, 'administrator successfully added.')

        return HttpResponseRedirect(reverse_lazy("home"))
