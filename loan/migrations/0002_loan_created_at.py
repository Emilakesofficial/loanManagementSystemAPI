# Generated by Django 5.1.6 on 2025-03-22 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("loan", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="loan",
            name="created_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
