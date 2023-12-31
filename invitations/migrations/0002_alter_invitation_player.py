# Generated by Django 4.1.9 on 2023-08-14 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("stat_track", "0003_alter_matchday_date_delete_joinrequest"),
        ("invitations", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invitation",
            name="player",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="invitation",
                to="stat_track.player",
            ),
        ),
    ]
