from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.detail import DetailView

from stat_track.decorators import is_league_owner
from stat_track.models import League, Player

from .models import Invitation


@login_required
@is_league_owner
def create_invitation(request, league_id, player_id):

    inviter = request.user

    print("\n", player_id, league_id, "\n")
    player = get_object_or_404(Player, pk=player_id)
    league = get_object_or_404(League, pk=league_id)

    #CREATE LOGIC TO CHECK IF THERE IS NO INVITATION FOR THIS PLAYER TO THIS LEAGUE EXCEPTING EXPIRED ONES
    
    invite = Invitation(
        inviter = inviter,
        player = player,
        league = league)

    invite.save()

    return redirect("invitation_detail", league.id, invite.id)


class InvitationDetail(DetailView):
    model = Invitation
    context_object_name = "invitation"
    template_name = "invitation/invitation_detail.html"

    def get_object(self, queryset=None):
        return Invitation.objects.get(id=self.kwargs.get('invite_id'))