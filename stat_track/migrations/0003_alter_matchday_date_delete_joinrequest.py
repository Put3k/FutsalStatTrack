# Generated by Django 4.1.9 on 2023-08-14 13:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stat_track", "0002_alter_player_leagues_joinrequest"),
    ]

    operations = [
        migrations.AlterField(
            model_name="matchday",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime.now, verbose_name="Date of match"
            ),
        ),
        migrations.DeleteModel(
            name="JoinRequest",
        ),
    ]
