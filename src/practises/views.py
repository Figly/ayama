from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from . import forms, models


class AddPractiseView(LoginRequiredMixin, generic.CreateView):
    template_name = "practises/add_practise_detail.html"
    form_class = forms.AddPractiseDetailForm
    model = models.PractiseDetail
    success_url = reverse_lazy("practises:add-advisor")
    form_valid_message = "Practise successfully added."

    def form_valid(self, form):
        model = form.save(commit=False)  # noqa
        return super(AddPractiseView, self).form_valid(form)


class AddAdvisorDetailView(LoginRequiredMixin, generic.CreateView):
    template_name = "practises/add_advisor_detail.html"
    form_class = forms.AddAdvisorDetailForm
    model = models.AdvisorDetail
    success_url = reverse_lazy("practises:add-advisor-contact")
    form_valid_message = "Advisor successfully added."

    def form_valid(self, form):
        model = form.save(commit=False)  # noqa
        return super(AddAdvisorDetailView, self).form_valid(form)


class AddAdvisorContactDetailView(LoginRequiredMixin, generic.CreateView):
    template_name = "practises/add_advisor_contact_detail.html"
    form_class = forms.AddAdvisorContactDetailForm
    model = models.AdvisorDetail
    success_url = reverse_lazy("home")
    form_valid_message = "Advisor contact details successfully added."

    def form_valid(self, form):
        model = form.save(commit=False)  # noqa
        return super(AddAdvisorContactDetailView, self).form_valid(form)


class AddAdministratorView(LoginRequiredMixin, generic.CreateView):
    template_name = "practises/add_administrator.html"
    form_class = forms.AddAdministratorDetailForm
    model = models.AdministratorDetail
    success_url = reverse_lazy("practises:add-administrator-contact")
    form_valid_message = "Advisor contact details successfully added."

    def form_valid(self, form):
        model = form.save(commit=False)  # noqa
        return super(AddAdministratorView, self).form_valid(form)


class AddAdministratorContactDetailView(LoginRequiredMixin, generic.CreateView):
    template_name = "practises/add_administrator_contact_detail.html"
    form_class = forms.AddAdministratorContactDetailForm
    model = models.AdministratorContactDetail
    success_url = reverse_lazy("home")
    form_valid_message = "Advisor contact details successfully added."

    def form_valid(self, form):
        model = form.save(commit=False)  # noqa
        return super(AddAdministratorContactDetailView, self).form_valid(form)
