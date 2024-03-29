# Generated by Django 4.2.1 on 2023-09-11 09:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("goals", "0005_alter_boardparticipant_board_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="boardparticipant",
            name="board",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="boardparticipants",
                to="goals.board",
                verbose_name="Board",
            ),
        ),
        migrations.AlterField(
            model_name="boardparticipant",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="boardparticipants",
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
    ]
