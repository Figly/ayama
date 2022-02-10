# Generated by Django 2.2.13 on 2021-04-29 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("practises", "0014_merge_20210308_0930"),
    ]

    operations = [
        migrations.AlterField(
            model_name="advisorcontactdetail",
            name="postal_address_line_1",
            field=models.CharField(max_length=100, verbose_name="Street Address"),
        ),
        migrations.AlterField(
            model_name="advisorcontactdetail",
            name="postal_address_line_2",
            field=models.CharField(
                blank=True,
                max_length=100,
                null=True,
                verbose_name="Apt, Suite, Building or Company Name (Optional)",
            ),
        ),
        migrations.AlterField(
            model_name="advisorcontactdetail",
            name="postal_city",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="City"
            ),
        ),
        migrations.AlterField(
            model_name="advisorcontactdetail",
            name="postal_country",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Country"
            ),
        ),
        migrations.AlterField(
            model_name="advisorcontactdetail",
            name="postal_suburb",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Suburb"
            ),
        ),
        migrations.AlterField(
            model_name="advisorcontactdetail",
            name="residential_address_line_1",
            field=models.CharField(max_length=100, verbose_name="Street Address"),
        ),
        migrations.AlterField(
            model_name="advisorcontactdetail",
            name="residential_address_line_2",
            field=models.CharField(
                blank=True,
                max_length=100,
                null=True,
                verbose_name="Apt, Suite, Building or Company Name (Optional)",
            ),
        ),
        migrations.AlterField(
            model_name="advisorcontactdetail",
            name="residential_city",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="City"
            ),
        ),
        migrations.AlterField(
            model_name="advisorcontactdetail",
            name="residential_code",
            field=models.IntegerField(verbose_name="Postal Code"),
        ),
        migrations.AlterField(
            model_name="advisorcontactdetail",
            name="residential_country",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Country"
            ),
        ),
        migrations.AlterField(
            model_name="advisorcontactdetail",
            name="residential_suburb",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Suburb"
            ),
        ),
        migrations.AlterField(
            model_name="advisordetail",
            name="practise_id_fk",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="practises.PractiseDetail",
            ),
        ),
        migrations.AlterOrderWithRespectTo(
            name="advisoremploymentdetail", order_with_respect_to="created_at",
        ),
    ]