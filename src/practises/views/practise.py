from braces.views import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic

from .. import forms, models


class AddPractiseView(LoginRequiredMixin, generic.CreateView):
    template_name = "practises/add_practise_detail.html"
    form_class = forms.AddPractiseDetailForm
    model = models.PractiseDetail

    def form_valid(self, form):
        model = form.save()

        messages.add_message(self.request, messages.SUCCESS, 'practise successfully added.')
        
        if 'add-advisor' in self.request.POST:
            self.success_url = reverse_lazy("practises:add-advisor", kwargs={'practise': model.id})
        elif 'submit' in self.request.POST:
            self.success_url = reverse_lazy("home")

        return super(AddPractiseView, self).form_valid(form)
