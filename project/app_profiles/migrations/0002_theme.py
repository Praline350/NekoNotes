# Generated by Django 5.1.1 on 2024-11-08 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_profiles", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Theme",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=120)),
                (
                    "colors",
                    models.ManyToManyField(
                        related_name="themes", to="app_profiles.color"
                    ),
                ),
            ],
        ),
    ]
