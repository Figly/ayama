from import_export import resources, fields, widgets
from django.contrib import admin, messages

from .models import (
    ClientContactDetail,
    ClientCommunication,
    ClientCommunicationFrequency,
    ClientDetail,
    ClientImport,
    EmploymentDetail,
    RatesAndReturn,
)
from practises.models import AdvisorDetail, AdvisorContactDetail


class ClientImportResource(resources.ModelResource):

    # Convert given values to choices in model
    title = fields.Field(attribute="get_title_display", column_name=("Title"))
    medical_aid = fields.Field(
        attribute="get_medical_aid_display", column_name=("Medical Aid")
    )
    group_life_cover = fields.Field(
        attribute="get_group_life_cover_display", column_name=("Group Life Cover")
    )

    # TODO : Allow employment date widget to convert excel dates to python dates
    # employment_date = fields.Field(attribute='employment_date', column_name='employment_date', widget=widgets.DateWidget("%Y-%m-%d"))
    class Meta:
        model = ClientImport
        exclude = [
            "id",
        ]
        import_id_fields = [
            "sa_id",
        ]
        skip_unchanged = True
        report_skipped = True

    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):

        if not dry_run:
            user = kwargs["user"]

            advisor_index = dataset.headers.index("advisor_email")
            sa_id_index = dataset.headers.index("sa_id")

            # Pull advisors within practise
            if user.is_superuser:
                advisors = AdvisorDetail.objects.all()
            elif user.is_administrator:
                practise_id = user.Administrator.practise_id_fk
                advisors = AdvisorDetail.objects.filter(practise_id_fk=practise_id)

            for row in dataset:
                # Determine whether client with similar sa_id is present in DB, skip row if true
                if (
                    ClientDetail.objects.all().filter(sa_id=row[sa_id_index]).count()
                    > 0
                ):
                    continue

                client_detail_dict = self.map_row_to_dict(
                    row, ClientDetail(), dataset.headers
                )
                employment_details_dict = self.map_row_to_dict(
                    row, EmploymentDetail(), dataset.headers
                )
                client_contact_dict = self.map_row_to_dict(
                    row, ClientContactDetail(), dataset.headers
                )

                # Get advisor id from email
                try:
                    advisor_contact_id = AdvisorContactDetail.objects.get(
                        email_address=row[advisor_index]
                    )
                    advisor = AdvisorDetail.objects.get(
                        advisor_contact_fk=advisor_contact_id.id
                    )

                    if advisor in advisors:
                        client_detail_dict["advisor_id_fk"] = advisor

                    else:
                        raise NameError(
                            f"Advisor {advisor} exists, but is not in this practise"
                        )

                except Exception as E:
                    raise NameError(f"Advisor {advisor} does not exist practise")
                    # TODO : Add message when advisor email not existing in DB
                    print(E)
                    continue

                self.save_models(
                    client_detail_dict,
                    employment_details_dict,
                    client_contact_dict,
                    user,
                )

    def map_row_to_dict(self, row, model, headers):
        # Assign values from csv to individual models that values belong to.
        model_fields = [field.name for field in model._meta.get_fields()]

        data_dict = {}
        for field in model_fields:
            if field != "id":
                for k, v in enumerate(headers):
                    if v == field:
                        data_dict[field] = row[k]
        return data_dict

    def save_models(
        self, client_detail_dict, employment_details_dict, client_contact_dict, user
    ):
        client = ClientDetail(**client_detail_dict)
        contactDetail = ClientContactDetail(**client_contact_dict)
        employmentDetail = EmploymentDetail(**employment_details_dict)
        rates = RatesAndReturn()
        clientComm = ClientCommunication()
        communicationFrequency = ClientCommunicationFrequency()

        contactDetail.modified_by = user
        contactDetail.save()

        employmentDetail.modified_by = user
        employmentDetail.save()

        rates.modified_by = user
        rates.save()

        clientComm.modified_by = user
        clientComm.save()
        client.client_comms_fk = clientComm

        advisorConfig = client.advisor_id_fk.reminder_config_freq_fk

        communicationFrequency.sms_frequency = advisorConfig.sms_frequency
        communicationFrequency.face_to_face_frequency = (
            advisorConfig.face_to_face_frequency
        )
        communicationFrequency.calls_frequency = advisorConfig.calls_frequency
        communicationFrequency.email_frequency = advisorConfig.email_frequency
        communicationFrequency.modified_by = user
        communicationFrequency.save()

        client.client_comms_freq_fk = communicationFrequency
        client.client_contact_fk = contactDetail
        client.client_employment_fk = employmentDetail
        client.client_rates_fk = rates
        client.modified_by = user
        client.save()
