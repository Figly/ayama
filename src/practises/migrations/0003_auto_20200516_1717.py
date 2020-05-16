# Generated by Django 2.2.6 on 2020-05-16 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practises', '0002_auto_20191208_1233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='administratordetail',
            name='advisor_id_fk',
        ),
        migrations.AlterField(
            model_name='administratorcontactdetail',
            name='email_address',
            field=models.EmailField(max_length=50, verbose_name='Email Address'),
        ),
        migrations.AlterField(
            model_name='administratordetail',
            name='employment_date',
            field=models.DateField(default='2018-01-01', verbose_name='Employment Date'),
        ),
        migrations.AlterField(
            model_name='advisorcontactdetail',
            name='email_address',
            field=models.EmailField(max_length=50, verbose_name='Email Address'),
        ),
    ]
