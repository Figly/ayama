from __future__ import unicode_literals

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Field, Layout, Row, Submit
from practises.models import AdvisorDetail

from ..models import ClientDetail


class AddClientDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields["advisor_id_fk"].label = "Advisor"
        self.fields["names"].label = "First Name"
        self.fields["surnames"].label = "Last Name"

        self.fields["advisor_id_fk"].widget.attrs["class"] = "figly-form-control"
        self.fields["title"].widget.attrs["class"] = "figly-form-control"
        self.fields["initials"].widget.attrs["class"] = "figly-form-control"
        self.fields["names"].widget.attrs["class"] = "figly-form-control"
        self.fields["surnames"].widget.attrs["class"] = "figly-form-control"
        self.fields["sa_id"].widget.attrs["class"] = "figly-form-control"
        self.fields["passport_no"].widget.attrs["class"] = "figly-form-control"

        self.helper.layout = Layout(
            Row(
                Column(
                    "advisor_id_fk",
                    placeholder="Advisor",
                    css_class="form-group col-md-10 ",
                ),
            ),
            Row(
                Column("title", placeholder="Title", css_class="form-group col-md-5"),
                Column(
                    "initials",
                    placeholder="Initials",
                    css_class="form-group col-md-5",
                ),
            ),
            Row(
                Column(
                    "names", placeholder="Name(s)", css_class="form-group col-md-10"
                ),
            ),
            Row(
                Column(
                    "surnames",
                    placeholder="Surname(s)",
                    css_class="form-group col-md-10",
                ),
            ),
            Row(
                Column(
                    "sa_id",
                    placeholder="RSA ID Number",
                    css_class="form-group col-md-10",
                ),
            ),
            Row(
                Column(
                    "passport_no",
                    placeholder="Passport Number",
                    css_class="form-group col-md-10",
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
