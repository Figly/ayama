from __future__ import unicode_literals

from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from . import models

class AddClientDetailView(LoginRequiredMixin, generic.CreateView):
    template_name = "clients/add_client_detail.html"
    form_class = forms.AddClientDetailForm
    model = models.ClientDetail
    success_url = reverse_lazy("clients:add-client-contact")
    form_valid_message = "Client successfully added."

    def form_valid(self, form):
        model = form.save(commit=False)
        return super(AddClientDetailView, self).form_valid(form)


class AddClientContactDetailView(LoginRequiredMixin, generic.CreateView):
    template_name = "clients/add_client_contact_detail.html"
    form_class = forms.AddClientContactDetailForm
    model = models.ClientDetail
    success_url = reverse_lazy("home")
    form_valid_message = "Client contact details successfully added."

    def form_valid(self, form):
        model = form.save(commit=False)
        return super(AddClientContactDetailView, self).form_valid(form)
