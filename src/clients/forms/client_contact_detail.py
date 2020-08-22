from __future__ import unicode_literals

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Field, Fieldset, Layout, Row, Submit
from practises.models import AdvisorDetail

from ..models import ClientContactDetail


class AddClientContactDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields["telephone_home"].widget.attrs["class"] = "figly-form-control"
        self.fields["telephone_work"].widget.attrs["class"] = "figly-form-control"
        self.fields["cellphone_number"].widget.attrs["class"] = "figly-form-control"
        self.fields["fax_number"].widget.attrs["class"] = "figly-form-control"
        self.fields["email_address"].widget.attrs["class"] = "figly-form-control"
        self.fields["residential_address_line_1"].widget.attrs[
            "class"
        ] = "figly-form-control"
        self.fields["residential_address_line_1"].widget.attrs[
            "id"
        ] = "residential-line-1-id"
        self.fields["residential_address_line_2"].widget.attrs[
            "class"
        ] = "figly-form-control"
        self.fields["residential_address_line_2"].widget.attrs[
            "id"
        ] = "residential-line-2-id"
        self.fields["residential_code"].widget.attrs["class"] = "figly-form-control"
        self.fields["residential_code"].widget.attrs["id"] = "residential-code-id"
        self.fields["postal_address_line_1"].widget.attrs[
            "class"
        ] = "figly-form-control"
        self.fields["postal_address_line_1"].widget.attrs["id"] = "postal-line-1-id"
        self.fields["postal_address_line_2"].widget.attrs[
            "class"
        ] = "figly-form-control"
        self.fields["postal_address_line_2"].widget.attrs["id"] = "postal-line-2-id"
        self.fields["postal_code"].widget.attrs["class"] = "figly-form-control"
        self.fields["postal_code"].widget.attrs["id"] = "postal-code-id"

        self.helper.layout = Layout(
            Row(
                Column(
                    "telephone_home",
                    placeholder="Home telephone number",
                    css_class="form-group col-md-10",
                )
            ),
            Row(
                Column(
                    "telephone_work",
                    placeholder="Work Telephone number",
                    css_class="form-group col-md-10",
                ),
            ),
            Row(
                Column(
                    "cellphone_number",
                    placeholder="Cellphone number",
                    css_class="form-group col-md-10",
                ),
            ),
            Row(
                Column(
                    "fax_number",
                    placeholder="Fax number",
                    css_class="form-group col-md-10",
                ),
            ),
            Row(
                Column(
                    "email_address",
                    placeholder="Email address",
                    css_class="form-group col-md-10",
                ),
            ),
            HTML("<hr/>"),
            HTML("<h3>Residential address</h3>"),
            Row(
                Column(
                    "residential_address_line_1",
                    placeholder="Residential Line 1",
                    css_class="form-group col-md-10",
                ),
            ),
            Row(
                Column(
                    "residential_address_line_2",
                    placeholder="Residential Line 2",
                    css_class="form-group col-md-10",
                ),
            ),
            Row(
                Column(
                    "residential_code",
                    placeholder="Residential Code",
                    css_class="form-group col-md-10",
                ),
            ),
            HTML("<hr/>"),
            HTML("<h3>Postal address</h3>"),
            HTML("<input id='same-as-residential' type='checkbox'/>"),
            HTML(
                "<label type='checkbox' class='form-check-label' for='same-as-residential' style='margin-left:10px'>Same as residential address</label>"
            ),
            Row(
                Column(
                    "postal_address_line_1",
                    placeholder="Postal Address Line 1",
                    css_class="form-group col-md-10",
                ),
            ),
            Row(
                Column(
                    "postal_address_line_2",
                    placeholder="Postal Address Line 2",
                    css_class="form-group col-md-10",
                ),
            ),
            Row(
                Column(
                    "postal_code",
                    placeholder="Postal Code",
                    css_class="form-group col-md-10",
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
