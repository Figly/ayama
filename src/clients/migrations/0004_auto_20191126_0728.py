# Generated by Django 2.2.6 on 2019-11-26 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_auto_20191126_0723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dependent',
            name='names',
            field=models.CharField(max_length=100, verbose_name='Names'),
        ),
        migrations.AlterField(
            model_name='dependent',
            name='surnames',
            field=models.CharField(max_length=100, verbose_name='Surnames'),
        ),
        migrations.AlterField(
            model_name='employmentdetail',
            name='personnel_number',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Personnel Number'),
        ),
    ]
