from __future__ import unicode_literals

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Field, Layout, Row, Submit
from django import forms

from practises.models import AdvisorDetail
from ..models import ClientContactDetail


class AddClientContactDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    "telephone_home",
                    placeholder="Home telephone number",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "telephone_work",
                    placeholder="Work Telephone number",
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
                    placeholder="Email address",
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
        model = ClientContactDetail
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
