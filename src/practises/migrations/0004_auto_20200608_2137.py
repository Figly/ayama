# Generated by Django 2.2.13 on 2020-06-08 19:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("practises", "0003_auto_20200605_1243"),
    ]

    operations = [
        migrations.AlterField(
            model_name="administratordetail",
            name="practise_id_fk",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="Practise",
                to="practises.PractiseDetail",
            ),
        ),
        migrations.AlterField(
            model_name="administratordetail",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                primary_key=True,
                related_name="Administrator",
                serialize=False,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="advisordetail",
            name="practise_id_fk",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="Advisors",
                to="practises.PractiseDetail",
            ),
        ),
        migrations.AlterField(
            model_name="advisordetail",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                primary_key=True,
                related_name="Advisor",
                serialize=False,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
