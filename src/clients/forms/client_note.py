from __future__ import unicode_literals

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Field, Layout, Row, Submit
from practises.models import AdvisorDetail

from ..models import ClientNote


class AddClientNoteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    "client_id_fk",
                    placeholder="Client",
                    css_class="form-group col-md-2 mb-0",
                )
            ),
            Row(
                Column(
                    "note_type",
                    placeholder="Type",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "title", placeholder="Title", css_class="form-group col-md-6 mb-0"
                ),
            ),
            Row(
                Column(
                    "body", placeholder="Body", css_class="form-group col-md-6 mb-0",
                ),
            ),
        )

    class Meta:
        model = ClientNote
        widgets = {
            'body': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }
        fields = [
            "client_id_fk",
            "title",
            "note_type",
            "body",
        ]
