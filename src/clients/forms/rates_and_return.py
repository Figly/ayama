from __future__ import unicode_literals

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Field, Layout, Row, Submit
from practises.models import AdvisorDetail

from ..models import RatesAndReturn


class AddClientRatesAndReturnForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    "inflation",
                    placeholder="Inflation Rate",
                    css_class="form-group col-md-10",
                ),
            ),
            Row(
                Column(
                    "interest",
                    placeholder="Interest Rate",
                    css_class="form-group col-md-10",
                ),
            ),
            Row(
                Column(
                    "return_rate",
                    placeholder="Return Rate",
                    css_class="form-group col-md-10",
                ),
            ),
        )

    class Meta:
        model = RatesAndReturn
        fields = [
            "inflation",
            "interest",
            "return_rate",
        ]
