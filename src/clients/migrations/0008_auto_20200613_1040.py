# Generated by Django 2.2.13 on 2020-06-13 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_auto_20200608_2137'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientCommunication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('last_date_email', models.DateField(verbose_name='Last date email')),
                ('last_date_sms', models.DateField(verbose_name='Last date SMS')),
                ('last_date_call', models.DateField(verbose_name='Last date call')),
                ('last_date_face_to_face', models.DateField(verbose_name='Last date face to face')),
            ],
            options={
                'get_latest_by': 'created_at',
                'abstract': False,
                'order_with_respect_to': 'created_at',
            },
        ),
        migrations.AddField(
            model_name='clientdetail',
            name='client_comms_fk',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='clients.ClientCommunication'),
            preserve_default=False,
        ),
    ]
