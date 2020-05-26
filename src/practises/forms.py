from __future__ import unicode_literals

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Field, Layout, Row, Submit
from django import forms

from .models import (
    AdministratorContactDetail,
    AdministratorDetail,
    AdvisorContactDetail,
    AdvisorDetail,
    PractiseDetail,
)


class AddPractiseDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field("name", placeholder="Name"),
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
            Submit("submit", "Submit", css_class="btn btn-lg btn-primary btn-block"),
        )

    class Meta:
        model = PractiseDetail
        fields = [
            "name",
            "residential_address_line_1",
            "residential_address_line_2",
            "residential_code",
            "postal_address_line_1",
            "postal_address_line_2",
            "postal_code",
        ]


class AddAdvisorDetailForm(forms.ModelForm):
    employment_date = forms.DateField(
        widget=forms.SelectDateWidget(
            empty_label=("Choose Year", "Choose Month", "Choose Day"),
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    "practise_id_fk",
                    placeholder="Practise",
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
            Submit("submit", "Submit", css_class="btn btn-lg btn-primary btn-block"),
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


class AddAdvisorContactDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Submit("submit", "Submit", css_class="btn btn-lg btn-primary btn-block"),
        )

    class Meta:
        model = AdvisorContactDetail
        fields = [
            "advisor_id_fk",
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


class AddAdministratorDetailForm(forms.ModelForm):
    employment_date = forms.DateField(
        widget=forms.SelectDateWidget(
            empty_label=("Choose Year", "Choose Month", "Choose Day"),
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    "practise_id_fk",
                    placeholder="Practise",
                    css_class="form-group col-md-2 mb-0",
                ),
                Column(
                    "advisor_id_fk",
                    placeholder="Practise",
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
            Submit("submit", "Submit", css_class="btn btn-lg btn-primary btn-block"),
        )

    class Meta:
        model = AdministratorDetail
        fields = [
            "practise_id_fk",
            "advisor_id_fk",
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


class AddAdministratorContactDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    "adminstrator_id_fk",
                    placeholder="Residential Line 1",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "telephone_home",
                    placeholder="Residential Line 1",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "telephone_work",
                    placeholder="Residential Line 1",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            Row(
                Column(
                    "cellphone_number",
                    placeholder="Residential Line 1",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "fax_number",
                    placeholder="Residential Line 1",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "email_address",
                    placeholder="Residential Line 1",
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
            Submit("submit", "Submit", css_class="btn btn-lg btn-primary btn-block"),
        )

    class Meta:
        model = AdministratorContactDetail
        fields = [
            "adminstrator_id_fk",
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
