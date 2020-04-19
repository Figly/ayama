from __future__ import unicode_literals
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from .models import ClientDetail, ClientContactDetail
from practises.models import AdvisorDetail

class AddClientDetailForm(forms.ModelForm):
    employment_date = forms.DateField(
        widget=forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day"), )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(

            Row(
                Column('advisor_id_fk', placeholder='Advisor',
                       css_class='form-group col-md-2 mb-0'),
                Column('title', placeholder='Title',
                       css_class='form-group col-md-2 mb-0'),
                Column('initials', placeholder='Initials',
                       css_class='form-group col-md-3 mb-0'),
                Column('names', placeholder='Name(s)',
                       css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('surnames', placeholder='Surname(s)',
                       css_class='form-group col-md-4 mb-0'),
                Column('known_as', placeholder='Known As',
                       css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('sa_id', placeholder='RSA ID Number',
                       css_class='form-group col-md-6 mb-0'),
                Column('passport_no', placeholder='Passport Number',
                       css_class='form-group col-md-6 mb-0'),
            ),

            Submit("submit", "Submit", css_class="btn btn-lg btn-primary btn-block"),
        )

    class Meta:
        model = ClientDetail
        fields = [
            'advisor_id_fk',
            'title',
            'initials',
            'surnames',
            'names',
            'known_as',
            'sa_id',
            'passport_no',
        ]


class AddClientContactDetailForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(

            Submit("submit", "Submit", css_class="btn btn-lg btn-primary btn-block"),
        )

    class Meta:
        model = ClientContactDetail
        fields = [
            'client_id_fk',
            'telephone_home',
            'telephone_work',
            'cellphone_number',
            'fax_number',
            'email_address',
            'residential_address_line_1',
            'residential_address_line_2',
            'residential_code',
            'postal_address_line_1',
            'postal_address_line_2',
            'postal_code',
        ]
