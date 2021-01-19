from __future__ import unicode_literals

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Field, Layout, Row, Submit
from django import forms

from practises.models import AdvisorDetail
from ..models import Dependent


class AddClientDependentDetailsForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.TextInput(attrs={"class": "datepicker"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields["client_id_fk"].widget.attrs["class"] = "figly-form-control"
        self.fields["relationship"].widget.attrs["class"] = "figly-form-control"
        self.fields["names"].widget.attrs["class"] = "figly-form-control"
        self.fields["surnames"].widget.attrs["class"] = "figly-form-control"
        self.fields["rsa_resident"].widget.attrs["class"] = "figly-form-control"
        self.fields["id_no"].widget.attrs["class"] = "figly-form-control"
        self.fields["date_of_birth"].widget.attrs["class"] = "figly-form-control"
        self.fields["other"].widget.attrs["class"] = "figly-form-control"
        self.helper.layout = Layout(
            Row(
                Column(
                    "client_id_fk",
                    placeholder="Client",
                    css_class="form-group col-md-5",
                ),
                Column(
                    "relationship",
                    placeholder="Relationship",
                    css_class="form-group col-md-5",
                ),
            ),
            Row(
                Column("names", placeholder="Names", css_class="form-group col-md-5"),
                Column(
                    "surnames",
                    placeholder="surnames",
                    css_class="form-group col-md-5",
                ),
            ),
            Row(
                Column(
                    "rsa_resident",
                    placeholder="RSA Resident",
                    css_class=" form-row-left-single-col col-md-5",
                ),
            ),
            Row(
                Column(
                    "id_no",
                    placeholder="ID Number",
                    css_class="form-group  col-md-5 ",
                ),
                Column(
                    "other",
                    placeholder="other",
                    css_class="form-group col-md-5 ",
                ),
            ),
            Row(
                Column(
                    "date_of_birth",
                    placeholder="Date Of Birth",
                    css_class="form-row-left-single-col col-md-5 calendar-dropdown",
                ),
            ),
        )

    class Meta:
        model = Dependent
        fields = [
            "client_id_fk",
            "names",
            "surnames",
            "rsa_resident",
            "id_no",
            "date_of_birth",
            "relationship",
            "other",
        ]
