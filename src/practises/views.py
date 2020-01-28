from __future__ import unicode_literals

from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from . import models


class AddPractiseView(LoginRequiredMixin, generic.CreateView):
    template_name = "practises/add_practise_detail.html"
    form_class = forms.AddPractiseDetailForm
    model = models.PractiseDetail
    success_url = reverse_lazy("practises:add-advisor")
    form_valid_message = "Practise successfully added."

    def form_valid(self, form):
        model = form.save(commit=False)
        return super(AddPractiseView, self).form_valid(form)


class AddAdvisorDetailView(LoginRequiredMixin, generic.CreateView):
    template_name = "practises/add_advisor_detail.html"
    form_class = forms.AddAdvisorDetailForm
    model = models.AdvisorDetail
    success_url = reverse_lazy("practises:add-advisor-contact")
    form_valid_message = "Advisor successfully added."

    def form_valid(self, form):
        model = form.save(commit=False)
        return super(AddAdvisorDetailView, self).form_valid(form)


class AddAdvisorContactDetailView(LoginRequiredMixin, generic.CreateView):
    template_name = "practises/add_advisor_contact_detail.html"
    form_class = forms.AddAdvisorContactDetailForm
    model = models.AdvisorDetail
    success_url = reverse_lazy("home")
    form_valid_message = "Advisor contact details successfully added."

    def form_valid(self, form):
        model = form.save(commit=False)
        return super(AddAdvisorContactDetailView, self).form_valid(form)
