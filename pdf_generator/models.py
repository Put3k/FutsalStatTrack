import uuid

from django.contrib.auth import get_user_model
from django.db import models

from stat_track.models import League

User = get_user_model()

class Report(models.Model):
    id = models.UUIDField(
        primary_key = True,
        default=uuid.uuid4,
        editable=False)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="reports")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports")
    generated = models.DateField()
    url = models.URLField(max_length=200)


    def __str__(self):
        return f"stat-track-report-{self.league}-{self.generated}"

