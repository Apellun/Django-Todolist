# Generated by Django 4.2.1 on 2023-09-11 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0004_rename_user_tguser_user_id_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="tguser",
            old_name="user_id",
            new_name="user",
        ),
    ]