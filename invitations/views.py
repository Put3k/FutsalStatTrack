from django.contrib import messages
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

    # Check if there is no active invitations for this player:
    invitations = Invitation.objects.filter(player=player, league=league)
    for invitation in invitations:
        if not invitation.expired:
            messages.error(request, "There is an active invitation linked to this player!")
            return redirect("players_list", league.id)
        if invitation.accepted:
            messages.error(request, "This player has already accepted the invitation.")
            return redirect("players_list", league.id)

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