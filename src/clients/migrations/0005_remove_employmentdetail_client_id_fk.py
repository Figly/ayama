# Generated by Django 2.2.6 on 2020-06-05 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_auto_20200605_1352'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employmentdetail',
            name='client_id_fk',
        ),
    ]