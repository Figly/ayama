from __future__ import unicode_literals

from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from . import models

class AddClientDetailView(LoginRequiredMixin, generic.CreateView):
    template_name = "clients/add_client_detail.html"
    form_class = forms.AddClientDetailForm
    model = models.ClientDetail
    form_valid_message = "Client successfully added."

    def form_valid(self, form):
        model = form.save(commit=False)
        return super(AddClientDetailView, self).form_valid(form)

    def get_success_url(self):
        return reverse('clients:add-client-contact', kwargs={'cid':self.object.id,})

class AddClientContactDetailView(LoginRequiredMixin, generic.CreateView):
    template_name = "clients/add_client_contact_detail.html"
    form_class = forms.AddClientContactDetailForm
    model = models.ClientContactDetail
    form_valid_message = "Client contact details successfully added."

    def get_initial(self):
        return {'client_id_fk': self.kwargs['cid']}

    def form_valid(self, form):
        model = form.save(commit=False)
        return super(AddClientContactDetailView, self).form_valid(form)

    def get_success_url(self):
        return reverse('clients:add-client-employment', kwargs={'cid':self.kwargs['cid'],})

class AddClientEmploymentDetailView(LoginRequiredMixin, generic.CreateView):
    template_name = "clients/add_client_employment_detail.html"
    form_class = forms.AddClientEmploymentetailForm
    model = models.EmploymentDetail
    form_valid_message = "Client employment details successfully added."

    def get_initial(self):
        return {'client_id_fk': self.kwargs['cid']}

    def form_valid(self, form):
        model = form.save(commit=False)
        return super(AddClientEmploymentDetailView, self).form_valid(form)

    def get_success_url(self):
        return reverse('clients:add-client-rates', kwargs={'cid':self.kwargs['cid'],})

class AddClientRatesView(LoginRequiredMixin, generic.CreateView):
    template_name = "clients/add_client_rates_detail.html"
    form_class = forms.AddClientRatesAndReturnForm
    model = models.RatesAndReturn
    success_url = reverse_lazy("clients:add-client-dependent")
    form_valid_message = "Client rates and return details successfully added."

    def get_initial(self):
        return {'client_id_fk': self.kwargs['cid']}

    def form_valid(self, form):
        model = form.save(commit=False)
        return super(AddClientRatesView, self).form_valid(form)

    def get_success_url(self):
        return reverse('clients:add-client-dependent', kwargs={'cid':self.kwargs['cid'],})

class AddClientDependentDetailView(LoginRequiredMixin, generic.CreateView):
    template_name = "clients/add_client_dependent_detail.html"
    form_class = forms.AddClientDependentDetailsForm
    model = models.Dependent
    success_url = reverse_lazy("home")
    form_valid_message = "Client dependent details successfully added."

    def get_initial(self):
        return {'client_id_fk': self.kwargs['cid']}

    def form_valid(self, form):
        model = form.save(commit=False)
        return super(AddClientDependentDetailView, self).form_valid(form)

