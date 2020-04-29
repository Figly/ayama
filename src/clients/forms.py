from __future__ import unicode_literals
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from .models import ClientDetail, ClientContactDetail, EmploymentDetail, RatesAndReturn, Dependent
from practises.models import AdvisorDetail

class AddClientDetailForm(forms.ModelForm):

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

            Row(
                Column('client_id_fk', placeholder='Client',
                       css_class='form-group col-md-6 mb-0'),

                Column('telephone_home', placeholder='Home telephone number',
                       css_class='form-group col-md-6 mb-0'),

                Column('telephone_work', placeholder='Work Telephone number',
                       css_class='form-group col-md-6 mb-0'),
                ),
            Row(
                Column('cellphone_number', placeholder='Cellphone number',
                       css_class='form-group col-md-6 mb-0'),

                Column('fax_number', placeholder='Fax number',
                       css_class='form-group col-md-6 mb-0'),

                Column('email_address', placeholder='Email address',
                       css_class='form-group col-md-6 mb-0'),
                ),


            Row(

                Column('residential_address_line_1', placeholder='Residential Line 1',
                       css_class='form-group col-md-6 mb-0'),
                Column('residential_address_line_2', placeholder='Residential Line 2',
                       css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('residential_code', placeholder='Residential Code',
                       css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('postal_address_line_1', placeholder='Postal Address Line 1',
                       css_class='form-group col-md-6 mb-0'),
                Column('postal_address_line_2', placeholder='Postal Address Line 2',
                       css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('postal_code', placeholder='Postal Code',
                       css_class='form-group col-md-3 mb-0'),
            ),

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

class AddClientEmploymentetailForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(

            Row(
                Column('client_id_fk', placeholder='Client',
                       css_class='form-group col-md-6 mb-0'),

                Column('company_name', placeholder='Company',
                       css_class='form-group col-md-6 mb-0'),

                Column('employment_date', placeholder='Employment Date',
                       css_class='form-group col-md-6 mb-0'),

              Column('personnel_number', placeholder='Personnel Number',
                       css_class='form-group col-md-6 mb-0'),
                ),
              Row(
                     Column('medical_aid', placeholder='Medical Aid',
                            css_class='form-group col-md-6 mb-0'),

                     Column('retirement_fund_current_value', placeholder='Retirement Fund Current Value',
                            css_class='form-group col-md-6 mb-0'),

                     Column('group_life_cover', placeholder='Group Life Cover',
                            css_class='form-group col-md-6 mb-0'),
                     ),
            Submit("submit", "Submit", css_class="btn btn-lg btn-primary btn-block"),
        )

    class Meta:
        model = EmploymentDetail
        fields = [
            'client_id_fk',
            'company_name',
            'employment_date',
            'personnel_number',
            'medical_aid',
            'retirement_fund_current_value',
            'group_life_cover',
        ]

class AddClientRatesAndReturnForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(

            Row(
                Column('client_id_fk', placeholder='Client',
                       css_class='form-group col-md-6 mb-0'),

                Column('inflation', placeholder='Inflation Rate',
                       css_class='form-group col-md-6 mb-0'),

                Column('interest', placeholder='Interest Rate',
                       css_class='form-group col-md-6 mb-0'),

              Column('return_rate', placeholder='Return Rate',
                       css_class='form-group col-md-6 mb-0'),
                ),
            Submit("submit", "Submit", css_class="btn btn-lg btn-primary btn-block"),
        )

    class Meta:
        model = RatesAndReturn
        fields = [
            'client_id_fk',
            'inflation',
            'interest',
            'return_rate',
        ]

class AddClientDependentDetailsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(

            Row(
                Column('client_id_fk', placeholder='Client',
                       css_class='form-group col-md-6 mb-0'),

                Column('names', placeholder='Names',
                       css_class='form-group col-md-6 mb-0'),

                Column('surnames', placeholder='surnames',
                       css_class='form-group col-md-6 mb-0'),

              Column('rsa_resident', placeholder='RSA Resident',
                       css_class='form-group col-md-6 mb-0'),
                ),
              Row(
                     Column('id_no', placeholder='ID Number',
                            css_class='form-group col-md-6 mb-0'),

                     Column('date_of_birth', placeholder='Date Of Birth',
                            css_class='form-group col-md-6 mb-0'),

                     Column('relationship', placeholder='Relationship',
                            css_class='form-group col-md-6 mb-0'),

                     Column('other', placeholder='Other',
                            css_class='form-group col-md-6 mb-0'),
                     ),
            Submit("submit", "Submit", css_class="btn btn-lg btn-primary btn-block"),
        )

    class Meta:
        model = Dependent
        fields = [
            'client_id_fk',
            'names',
            'surnames',
            'rsa_resident',
            'id_no',
            'date_of_birth',
            'relationship',
            'other',
        ]
