# Generated by Django 5.0.6 on 2024-05-30 20:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="phone_number",
        ),
    ]
