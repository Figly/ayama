from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import construct_instance
from django.http.response import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from formtools.wizard.views import SessionWizardView
from practises.models import AdvisorDetail

from ..forms import AddClientNoteForm
from ..models import ClientDetail, ClientNote


class AddClientNoteView(LoginRequiredMixin, generic.CreateView):
    template_name = "clients/add_client_note.html"
    form_class = AddClientNoteForm
    model = ClientNote

    def get_form(self, *args, **kwargs):
        form = super(AddClientNoteView, self).get_form(*args, **kwargs)
        user = self.request.user
        if user.is_advisor:
            advisor_id = user.id  # noqa
            form.fields["client_id_fk"].queryset = user.Advisor.clients
        elif user.is_administrator:
            advisors = AdvisorDetail.objects.filter(
                practise_id_fk=user.Administrator.practise_id_fk
            )
            form.fields["client_id_fk"].queryset = ClientDetail.objects.filter(
                advisor_id_fk__in=advisors
            )
        return form

    def form_valid(self, form):
        model = form.save(commit=False)  # noqa
        model.modified_by = self.request.user
        messages.add_message(
            self.request, messages.SUCCESS, "client note successfully  added."
        )
        if "add-another" in self.request.POST:
            self.success_url = reverse_lazy("clients:add-client-note")
        elif "submit" in self.request.POST:
            self.success_url = reverse_lazy("home")
        return super(AddClientNoteView, self).form_valid(form)


class EditClientNoteView(LoginRequiredMixin, generic.UpdateView):
    template_name = "clients/edit_details.html"
    model = ClientNote
    fields = (
        "title",
        "note_type",
        "body",
    )

    def form_valid(self, form):
        if "cancel" in self.request.POST:
            url = reverse_lazy("home")
            return HttpResponseRedirect(url)

        model = form.save(commit=False)
        model.modified_by = self.request.user
        model.save

        messages.add_message(
            self.request, messages.SUCCESS, "client note successfully edited."
        )
        self.success_url = reverse_lazy("home")
        return super(EditClientNoteView, self).form_valid(form)


class ClientNoteListView(LoginRequiredMixin, generic.ListView):
    template_name = "clients/client_note_list.html"
    model = ClientNote

    def get_context_data(self, **kwargs):
        context = super(ClientNoteListView, self).get_context_data(**kwargs)
        client_id = self.kwargs["pk"]
        notes = ClientNote.objects.all().filter(client_id_fk_id=client_id)
        client = ClientDetail.objects.get(id=client_id)

        context = {
            "notes": notes,
            "client": client,
        }

        return context
