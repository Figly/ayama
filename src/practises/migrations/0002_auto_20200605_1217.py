# Generated by Django 2.2.6 on 2020-06-05 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('practises', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='administratorcontactdetail',
            name='adminstrator_id_fk',
        ),
        migrations.RemoveField(
            model_name='advisorcontactdetail',
            name='advisor_id_fk',
        ),
        migrations.AddField(
            model_name='administratordetail',
            name='adminstrator_contact_fk',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='practises.AdministratorContactDetail'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='advisordetail',
            name='advisor_contact_fk',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='practises.AdvisorDetail'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='advisordetail',
            name='practise_id_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='practises.AdvisorContactDetail'),
        ),
    ]
