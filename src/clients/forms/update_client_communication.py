from __future__ import unicode_literals

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Field, Layout, Row, Submit
from practises.models import AdvisorDetail

from ..models import ClientCommunication


class UpdateClientCommunicationHistory(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    "last_date_email",
                    placeholder="Last email date",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "last_date_sms",
                    placeholder="Last sms date",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "last_date_call",
                    placeholder="Last call date",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "last_date_face_to_face",
                    placeholder="Last face to face date",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
        )

    class Meta:
        widgets = {
            "last_date_email": forms.TextInput(attrs={"class": "datepicker"}),
            "last_date_sms": forms.TextInput(attrs={"class": "datepicker"}),
            "last_date_call": forms.TextInput(attrs={"class": "datepicker"}),
            "last_date_face_to_face": forms.TextInput(attrs={"class": "datepicker"}),
        }
        model = ClientCommunication
        fields = [
            "last_date_email",
            "last_date_sms",
            "last_date_call",
            "last_date_face_to_face",
        ]
