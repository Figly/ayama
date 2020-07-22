# Generated by Django 2.2.13 on 2020-07-22 13:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("practises", "0010_auto_20200716_2243"),
        ("clients", "0017_auto_20200716_2217"),
    ]

    operations = [
        migrations.CreateModel(
            name="ClientProduct",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "client_id_fk",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="clients.ClientDetail",
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "product_id_fk",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="practises.ProductDetail",
                    ),
                ),
            ],
            options={
                "get_latest_by": "created_at",
                "abstract": False,
                "order_with_respect_to": "created_at",
            },
        ),
    ]