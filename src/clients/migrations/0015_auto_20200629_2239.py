# Generated by Django 2.2.13 on 2020-06-29 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0014_clientnote"),
    ]

    operations = [
        migrations.AlterField(
            model_name="clientdetail",
            name="client_comms_fk",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to="clients.ClientCommunication",
            ),
        ),
        migrations.AlterField(
            model_name="clientdetail",
            name="client_comms_freq_fk",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to="clients.ClientCommunicationFrequency",
            ),
        ),
        migrations.AlterField(
            model_name="clientnote",
            name="body",
            field=models.TextField(verbose_name="Note"),
        ),
    ]