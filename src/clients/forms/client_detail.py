from __future__ import unicode_literals

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Field, Layout, Row, Submit
from django import forms

from practises.models import AdvisorDetail
from ..models import ClientDetail


class AddClientDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    "advisor_id_fk",
                    placeholder="Advisor",
                    css_class="form-group col-md-2 mb-0",
                ),
                Column(
                    "title", placeholder="Title", css_class="form-group col-md-2 mb-0"
                ),
                Column(
                    "initials",
                    placeholder="Initials",
                    css_class="form-group col-md-3 mb-0",
                ),
                Column(
                    "names", placeholder="Name(s)", css_class="form-group col-md-3 mb-0"
                ),
            ),
            Row(
                Column(
                    "surnames",
                    placeholder="Surname(s)",
                    css_class="form-group col-md-4 mb-0",
                ),
                Column(
                    "known_as",
                    placeholder="Known As",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            Row(
                Column(
                    "sa_id",
                    placeholder="RSA ID Number",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "passport_no",
                    placeholder="Passport Number",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
        )

    class Meta:
        model = ClientDetail
        fields = [
            "advisor_id_fk",
            "title",
            "initials",
            "surnames",
            "names",
            "known_as",
            "sa_id",
            "passport_no",
        ]
