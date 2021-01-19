from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Field, Layout, Row, Submit
from django import forms

from ..models import (
    AdvisorContactDetail,
    AdvisorDetail,
)


class AddAdvisorDetailForm(forms.ModelForm):
    employment_date = forms.DateField(
        widget=forms.TextInput(attrs={"class": "datepicker"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields["practise_id_fk"].widget.attrs["class"] = "figly-form-control"

        self.fields["title"].widget.attrs["class"] = "figly-form-control"
        self.fields["initials"].widget.attrs["class"] = "figly-form-control"
        self.fields["names"].widget.attrs["class"] = "figly-form-control"
        self.fields["surnames"].widget.attrs["class"] = "figly-form-control"
        self.fields["known_as"].widget.attrs["class"] = "figly-form-control"
        self.fields["sa_id"].widget.attrs["class"] = "figly-form-control"
        self.fields["passport_no"].widget.attrs["class"] = "figly-form-control"
        self.helper.layout = Layout(
            Row(
                Column(
                    "practise_id_fk",
                    placeholder="Practise",
                    css_class="form-group col-md-10 ",
                ),
            ),
            Row(
                Column(
                    "title",
                    placeholder="Title",
                    css_class="form-group col-md-5 figly-left-form-input",
                ),
                Column(
                    "initials",
                    placeholder="Initials",
                    css_class="form-group col-md-5 figly-right-form-input",
                ),
            ),
            Row(
                Column(
                    "names", placeholder="Name(s)", css_class="form-group col-md-10 "
                ),
            ),
            Row(
                Column(
                    "surnames",
                    placeholder="Surname(s)",
                    css_class="form-group col-md-10 ",
                ),
            ),
            Row(
                Column(
                    "known_as",
                    placeholder="Known As",
                    css_class="form-group col-md-10 ",
                ),
            ),
            Row(
                Column(
                    "sa_id",
                    placeholder="RSA ID Number",
                    css_class="form-group col-md-10 ",
                ),
            ),
            Row(
                Column(
                    "passport_no",
                    placeholder="Passport Number",
                    css_class="form-group col-md-10 ",
                ),
            ),
            Row(
                Column(
                    "position",
                    placeholder="Position",
                    css_class="form-group col-md-5 mb-0",
                ),
                Column(
                    "employment_date",
                    placeholder="Employment Date",
                    css_class="form-group col-md-4 mb-0",
                ),
                Column(
                    "personnel_number",
                    placeholder="Personnel Number",
                    css_class="form-group col-md-3 mb-0",
                ),
            ),
        )

    class Meta:
        model = AdvisorDetail
        fields = [
            "practise_id_fk",
            "title",
            "initials",
            "surnames",
            "names",
            "known_as",
            "sa_id",
            "passport_no",
            "position",
            "employment_date",
            "personnel_number",
        ]


class SignUpAdvisorDetailForm(forms.ModelForm):
    employment_date = forms.DateField(
        widget=forms.TextInput(attrs={"class": "datepicker"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
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
            Row(
                Column(
                    "position",
                    placeholder="Position",
                    css_class="form-group col-md-5 mb-0",
                ),
                Column(
                    "employment_date",
                    placeholder="Employment Date",
                    css_class="form-group col-md-4 mb-0",
                ),
                Column(
                    "personnel_number",
                    placeholder="Personnel Number",
                    css_class="form-group col-md-3 mb-0",
                ),
            ),
        )

    class Meta:
        model = AdvisorDetail
        fields = [
            "title",
            "initials",
            "surnames",
            "names",
            "known_as",
            "sa_id",
            "passport_no",
            "position",
            "employment_date",
            "personnel_number",
        ]


class AddAdvisorContactDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    "telephone_home",
                    placeholder="Telephone home",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "telephone_work",
                    placeholder="Telephone work",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            Row(
                Column(
                    "cellphone_number",
                    placeholder="Cellphone number",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "fax_number",
                    placeholder="Fax number",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "email_address",
                    placeholder="Email",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            Row(
                Column(
                    "residential_address_line_1",
                    placeholder="Residential Line 1",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "residential_address_line_2",
                    placeholder="Residential Line 2",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            Row(
                Column(
                    "residential_code",
                    placeholder="Residential Code",
                    css_class="form-group col-md-3 mb-0",
                ),
            ),
            Row(
                Column(
                    "postal_address_line_1",
                    placeholder="Postal Address Line 1",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "postal_address_line_2",
                    placeholder="Postal Address Line 2",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            Row(
                Column(
                    "postal_code",
                    placeholder="Postal Code",
                    css_class="form-group col-md-3 mb-0",
                ),
            ),
        )

    class Meta:
        model = AdvisorContactDetail
        fields = [
            "telephone_home",
            "telephone_work",
            "cellphone_number",
            "fax_number",
            "email_address",
            "residential_address_line_1",
            "residential_address_line_2",
            "residential_code",
            "postal_address_line_1",
            "postal_address_line_2",
            "postal_code",
        ]
