from __future__ import unicode_literals

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Field, Layout, Row, Submit
from django import forms

from practises.models import AdvisorDetail
from ..models import EmploymentDetail


class AddClientEmploymentetailForm(forms.ModelForm):
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
                    "company_name",
                    placeholder="Company",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "employment_date",
                    placeholder="Employment Date",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "personnel_number",
                    placeholder="Personnel Number",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            Row(
                Column(
                    "medical_aid",
                    placeholder="Medical Aid",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "retirement_fund_current_value",
                    placeholder="Retirement Fund Current Value",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "group_life_cover",
                    placeholder="Group Life Cover",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
        )

    class Meta:
        model = EmploymentDetail
        fields = [
            "company_name",
            "employment_date",
            "personnel_number",
            "medical_aid",
            "retirement_fund_current_value",
            "group_life_cover",
        ]
