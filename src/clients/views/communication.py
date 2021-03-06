import logging
from datetime import datetime

from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic

from ..forms import UpdateClientCommunicationHistory
from ..models import ClientCommunication, ClientCommunicationFrequency

log = logging.getLogger(__name__)


class EditClientCommunicationFrequencyView(LoginRequiredMixin, generic.UpdateView):
    template_name = "clients/edit_details.html"
    model = ClientCommunicationFrequency
    fields = (
        "face_to_face_frequency",
        "calls_frequency",
        "email_frequency",
        "sms_frequency",
    )

    def form_valid(self, form):
        if "cancel" in self.request.POST:
            url = reverse_lazy("home")
            return HttpResponseRedirect(url)

        model = form.save(commit=False)
        model.modified_by = self.request.user
        model.save

        messages.add_message(
            self.request,
            messages.SUCCESS,
            "client communication frequency successfully edited.",
        )
        self.success_url = reverse_lazy("home")
        return super(EditClientCommunicationFrequencyView, self).form_valid(form)


class UpdateClientCommunicationHistoryView(LoginRequiredMixin, generic.UpdateView):
    template_name = "clients/edit_details.html"
    model = ClientCommunication
    form_class = UpdateClientCommunicationHistory

    def form_valid(self, form):
        home = reverse_lazy("home")

        if "cancel" in self.request.POST:
            return HttpResponseRedirect(home)

        model = form.save(commit=False)

        today = datetime.date.today()
        if (
            model.last_date_email > today
            or model.last_date_sms > today
            or model.last_date_call > today
            or model.last_date_face_to_face > today
        ):
            messages.add_message(
                self.request, messages.ERROR, "Dates cannot be in the future.",
            )
            return HttpResponseRedirect(self.request.path_info)

        model.modified_by = self.request.user
        model.save

        messages.add_message(
            self.request,
            messages.SUCCESS,
            "client communication history successfully updated.",
        )
        self.success_url = home
        return super(UpdateClientCommunicationHistoryView, self).form_valid(form)


class UpdateLastSeen(generic.View):
    def post(self, request, *args, **kwargs):
        try:
            client_comms_id = request.POST.get("client_comms_id", None)
            date_value = request.POST.get("date_value")

            if client_comms_id is None:
                return JsonResponse({"valid": False}, status=400)

            clientComms = get_object_or_404(ClientCommunication, pk=client_comms_id)
            clientComms.last_contacted = date_value

            clientComms.save()

            return JsonResponse({"valid": True}, status=200)
        except Exception as e:
            log.info(e)
            return JsonResponse(
                {"valid": "An error occured. Please contact an administrator"},
                status=400,
            )
