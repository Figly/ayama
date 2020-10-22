from __future__ import unicode_literals

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Field, Layout, Row, Submit
from practises.models import AdvisorDetail

from ..models import EmploymentDetail


class AddClientEmploymentDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields["company_name"].widget.attrs["class"] = "figly-form-control"
        self.fields["employment_date"].widget.attrs[
            "class"
        ] = "figly-form-control datepicker"
        self.fields["personnel_number"].widget.attrs["class"] = "figly-form-control"
        self.fields["medical_aid"].widget.attrs["class"] = "figly-form-control"
        self.fields["retirement_fund_current_value"].widget.attrs[
            "class"
        ] = "figly-form-control"
        self.fields["group_life_cover"].widget.attrs["class"] = "figly-form-control"

        self.helper.layout = Layout(
            Row(
                Column(
                    "company_name",
                    placeholder="Company",
                    css_class="form-group col-md-10",
                ),
            ),
            Row(
                Column(
                    "employment_date",
                    placeholder="Employment Date",
                    css_class="form-group col-md-10",
                ),
            ),
            Row(
                Column(
                    "personnel_number",
                    placeholder="Personnel Number",
                    css_class="form-group col-md-10",
                ),
            ),
            Row(
                Column(
                    "medical_aid",
                    placeholder="Medical Aid",
                    css_class="form-group col-md-10",
                ),
            ),
            Row(
                Column(
                    "retirement_fund_current_value",
                    placeholder="Retirement Fund Current Value",
                    css_class="form-group col-md-10",
                ),
            ),
            Row(
                Column(
                    "group_life_cover",
                    placeholder="Group Life Cover",
                    css_class="form-group col-md-10",
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
