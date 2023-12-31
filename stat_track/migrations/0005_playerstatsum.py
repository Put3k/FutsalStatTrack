# Generated by Django 4.1.9 on 2023-11-03 10:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("stat_track", "0004_alter_player_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="PlayerStatSum",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("goals", models.PositiveIntegerField(default=0)),
                ("match_count", models.PositiveIntegerField(default=0)),
                ("matchday_count", models.PositiveIntegerField(default=0)),
                ("points", models.PositiveIntegerField(default=0)),
                ("wins", models.PositiveIntegerField(default=0)),
                ("loses", models.PositiveIntegerField(default=0)),
                ("draws", models.PositiveIntegerField(default=0)),
                (
                    "league",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="stat_track.league",
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="stat_track.player",
                    ),
                ),
            ],
        ),
    ]
