# Generated by Django 5.1.1 on 2024-11-18 15:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_dashboards", "0002_emptywidget"),
        ("app_widgets", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="simpletodolist",
            name="dashboard",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="simple_todo_list",
                to="app_dashboards.dashboard",
            ),
        ),
    ]