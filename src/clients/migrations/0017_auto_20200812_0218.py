# Generated by Django 2.2.13 on 2020-08-12 00:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0016_merge_20200703_2132"),
    ]

    operations = [
        migrations.CreateModel(
            name="ClientImport",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "advisor_email",
                    models.EmailField(
                        max_length=50, verbose_name="Advisor Email Address"
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        choices=[
                            ("mr", "Mister"),
                            ("mrs", "Misses"),
                            ("ms", "Miss"),
                            ("dr", "Doctor"),
                            ("prof", "Professor"),
                        ],
                        default="not specified",
                        max_length=30,
                        verbose_name="Title",
                    ),
                ),
                ("initials", models.CharField(max_length=10, verbose_name="Initials")),
                ("surnames", models.CharField(max_length=100, verbose_name="Surname")),
                ("names", models.CharField(max_length=100, verbose_name="Name")),
                (
                    "known_as",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="Known As"
                    ),
                ),
                ("sa_id", models.BigIntegerField(verbose_name="RSA ID Number")),
                (
                    "passport_no",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="Passport Number",
                    ),
                ),
                (
                    "company_name",
                    models.CharField(max_length=50, verbose_name="Company Name"),
                ),
                (
                    "occupation",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="Occupation"
                    ),
                ),
                (
                    "personnel_number",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="Personnel Number",
                    ),
                ),
                (
                    "medical_aid",
                    models.CharField(
                        choices=[("yes", "Yes"), ("no", "No")],
                        default="no",
                        max_length=5,
                        verbose_name="Medical Aid",
                    ),
                ),
                (
                    "retirement_fund_current_value",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=20,
                        null=True,
                        verbose_name="Retirement Fund Current Value",
                    ),
                ),
                (
                    "group_life_cover",
                    models.CharField(
                        choices=[("yes", "Yes"), ("no", "No")],
                        default="no",
                        max_length=5,
                        verbose_name="Group Life Cover",
                    ),
                ),
                (
                    "telephone_home",
                    models.CharField(
                        blank=True,
                        max_length=10,
                        null=True,
                        verbose_name="Home Telephone Number",
                    ),
                ),
                (
                    "telephone_work",
                    models.CharField(
                        blank=True,
                        max_length=10,
                        null=True,
                        verbose_name="Work Telephone Number",
                    ),
                ),
                (
                    "cellphone_number",
                    models.CharField(max_length=10, verbose_name="Cellphone Number"),
                ),
                (
                    "fax_number",
                    models.CharField(
                        blank=True, max_length=10, null=True, verbose_name="Fax Number"
                    ),
                ),
                (
                    "email_address",
                    models.EmailField(max_length=50, verbose_name="Email Address"),
                ),
                (
                    "residential_address_line_1",
                    models.CharField(
                        max_length=100, verbose_name="Residential Address 1"
                    ),
                ),
                (
                    "residential_address_line_2",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Residential Address 2",
                    ),
                ),
                (
                    "residential_code",
                    models.IntegerField(verbose_name="Residential Code"),
                ),
                (
                    "postal_address_line_1",
                    models.CharField(max_length=100, verbose_name="Postal Address 1"),
                ),
                (
                    "postal_address_line_2",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Postal Addres 2",
                    ),
                ),
                ("postal_code", models.IntegerField(verbose_name="Postal Code")),
            ],
        ),
        migrations.AlterField(
            model_name="clientdetail",
            name="client_comms_fk",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="client",
                to="clients.ClientCommunication",
            ),
        ),
    ]
