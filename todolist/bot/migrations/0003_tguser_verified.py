# Generated by Django 4.2.1 on 2023-09-05 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0002_tguser_verification_code_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="tguser",
            name="verified",
            field=models.BooleanField(
                default=False, verbose_name="Verified in the app"
            ),
        ),
    ]
