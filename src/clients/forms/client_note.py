from __future__ import unicode_literals

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Field, Layout, Row, Submit
from django import forms

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
                    "note_type", placeholder="Note Type", css_class="form-group col-md-6 mb-0"
                ),
                Column(
                    "title", placeholder="Title", css_class="form-group col-md-6 mb-0"
                ),
            ),
            Row(
                Column(
                    "body",
                    placeholder="Note",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
        )

    class Meta:
        model = ClientNote
        fields = [
            "client_id_fk",
            "note_type",
            "title",
            "body",
        ]
