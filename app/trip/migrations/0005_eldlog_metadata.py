# Generated by Django 5.1.7 on 2025-03-26 13:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("trip", "0004_rename_cycle_hours_trip_current_cycle"),
    ]

    operations = [
        migrations.AddField(
            model_name="eldlog",
            name="metadata",
            field=models.JSONField(blank=True, null=True),
        ),
    ]
