# Generated by Django 5.0.3 on 2024-06-18 18:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("utm_tracker", "0011_traffic_ip_address"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitehit",
            name="source",
            field=models.ForeignKey(
                blank=True,
                default="direct",
                null=True,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to="utm_tracker.source",
            ),
        ),
    ]
