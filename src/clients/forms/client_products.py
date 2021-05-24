import logging

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Field, Fieldset, Layout, Row, Submit
from django import forms
from django.db.models.functions import Lower
from practises.models import ProductAdvisor, ProductClient, ProductDetail


class AddClientProductsForm(forms.ModelForm):
    def __init__(self, advisor_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        # if self.instance:
        #     self.fields['product_id_fk'].initial = [c.id for c in ProductAdvisor.objects.filter(advisor_id_fk=advisor_id)]

        advisorProducts = ProductAdvisor.objects.filter(
            advisor_id_fk=advisor_id
        ).values_list("product_id_fk", flat=True)
        products = ProductDetail.objects.filter(id__in=advisorProducts)
        self.fields["product_id_fk"] = forms.ModelMultipleChoiceField(
            queryset=products, required=True, widget=forms.CheckboxSelectMultiple,
        )
        #

    class Meta:
        model = ProductClient
        fields = ["product_id_fk"]
