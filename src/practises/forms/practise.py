from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Field, Layout, Row, Submit
from django import forms

from ..models import PractiseDetail


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
