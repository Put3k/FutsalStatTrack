import datetime
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.db import models
from django.urls import reverse
from django.utils import timezone

from stat_track.models import League, Player

User = get_user_model()


class Invitation(models.Model):
    id = models.UUIDField(
        primary_key = True,
        default=uuid.uuid4,
        editable=False)
    
    accepted = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    inviter = models.ForeignKey(to=User, on_delete=models.CASCADE)
    player = models.ForeignKey(to=Player, related_name="invitation", on_delete=models.CASCADE)
    league = models.ForeignKey(to=League, on_delete=models.CASCADE)
    

    def __str__(self):
        return str(self.id)

    @property
    def expired(self):
        expiration_date = self.created + datetime.timedelta(
            days=3)
        return expiration_date <= timezone.now()

    @property
    def is_active(self):
        if self.expired or self.accepted:
            return False
        else:
            return True

    @property
    def key(self):
        return str(self.id) + str(self.player.id)

    # NOT IN USE DUE TO REQUEST
    # def accept_url(self, request):
    #     url = reverse('invitation_accept', kwargs={'league_id': self.league.id, 'key': self.key})
    #     return request.build_absolute_uri(url)

    @property
    def accept_url(self):
        host = settings.HOST
        url = reverse('invitation_accept', kwargs={'league_id': self.league.id, 'key': self.key})
        return ''.join([host, url])