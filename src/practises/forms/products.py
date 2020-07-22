from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Field, Layout, Row, Submit

from ..models import ProductDetail


class AddPrductDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    "product_type",
                    placeholder="Product Type",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "product_name",
                    placeholder="Product Name",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            Row(
                Column(
                    "product_company",
                    placeholder="Product Company",
                    css_class="form-group col-md-3 mb-0",
                ),
            ),
            Row(
                Column(
                    "is_active",
                    placeholder="Is Active",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
        )

    class Meta:
        model = ProductDetail
        fields = [
            "product_type",
            "product_name",
            "product_company",
            "is_active",
        ]
