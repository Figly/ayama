from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import construct_instance
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from formtools.wizard.views import SessionWizardView

from ..forms import AddAdvisorContactDetailForm, AddAdvisorDetailForm
from ..models import AdvisorContactDetail, AdvisorDetail

FORMS =[('0', AddAdvisorDetailForm),
        ('1', AddAdvisorContactDetailForm),]

TEMPLATES = {"0":"practises/add_advisor_detail.html",
        "1":"practises/add_advisor_contact_detail.html"}

class AdvisorWizard(SessionWizardView):
    def get_template_names(self):
        return TEMPLATES[self.steps.current]

    def dispatch(self, request, *args, **kwargs):
            self.practise = kwargs.get('practise', None)
            return super(AdvisorWizard, self).dispatch(request, *args, **kwargs)

    def get_form_initial(self, step):
        if self.steps.current == '0' and  self.practise is not None:
            initial = self.initial_dict.get(self.steps.current, {})
            return self.initial_dict.get(step, {'practise_id_fk':  self.practise})


    def get_context_data(self, form, **kwargs):
        context = super(AdvisorWizard, self).get_context_data(form=form, **kwargs)

        if self.steps.current != '0':
            advisor_name = []
            step0data = self.get_cleaned_data_for_step('0')
            advisor_name.append(step0data["title"].capitalize())
            advisor_name.append(step0data["initials"].capitalize())
            advisor_name.append(step0data["surnames"].capitalize())
            context.update({'advisor_name':' '.join(advisor_name)})
        return context

    def done(self, form_list, form_dict,**kwargs):
        #models backing db
        advisor = AdvisorDetail()
        advisorContact = AdvisorContactDetail()

        #form instances            
        advisor = construct_instance(form_dict["0"], advisor, form_dict["0"]._meta.fields, form_dict["0"]._meta.exclude)
        advisor.save()

        advisorContact = construct_instance(form_dict["1"], advisorContact, form_dict["1"]._meta.fields, form_dict["1"]._meta.exclude)
        advisorContact.advisor_id_fk = advisor
        advisorContact.save()

        messages.add_message(self.request, messages.SUCCESS, 'advisor successfully added.')

        return HttpResponseRedirect(reverse_lazy("home"))
