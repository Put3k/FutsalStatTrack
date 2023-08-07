import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.detail import DetailView

from stat_track.decorators import is_league_owner
from stat_track.models import League, MatchDayTicket, Player, Stat

from .models import Invitation


@login_required
@is_league_owner
def create_invitation(request, league_id, player_id):

    inviter = request.user

    player = get_object_or_404(Player, pk=player_id)
    league = get_object_or_404(League, pk=league_id)

    # Check if there is no active invitations for this player:
    invitations = Invitation.objects.filter(player=player, league=league)
    for invitation in invitations:
        if not invitation.expired:
            messages.error(request, "There is an active invitation linked to this player!")
            return redirect("players_list", league.id)

        #(IN CASE USER ASSIGNMENT GOES WRONG)
        if invitation.accepted:
            messages.error(request, "This player has already accepted the invitation.")
            return redirect("players_list", league.id)

    invite = Invitation(
        inviter = inviter,
        player = player,
        league = league)

    invite.save()

    return redirect("invitation_detail", league.id, invite.id)


def accept_invitation(request, league_id, key):

    invitation_id = uuid.UUID(key[:-36])
    player_id = uuid.UUID(key[36:])

    league = get_object_or_404(League, pk=league_id)
    invitation = get_object_or_404(Invitation, pk=invitation_id)
    player = get_object_or_404(Player, pk=player_id)
    request.session['player'] = key[36:]

    if request.method == 'POST':
        user_player = Player.objects.get(user=request.user)

        # If player associated with user is already connected to this league, he cannot join.
        if league in user_player.leagues.all():
            messages.error(request, "You already participate in that league!")
            return redirect('home')

        # If user has an account and accepts invitation, existing player stats are merged into user.player and old player is deleted.
        if request.POST.get('mergeUser', ''):
            Stat.objects.filter(player=player).update(player=user_player)
            MatchDayTicket.objects.filter(player=player).update(player=user_player)
            leagues = player.leagues.all()
            user_player.leagues.add(*leagues)

            player.delete()
            return redirect('home')

    context = {
        "player": player,
        "league": league,
        "key": key,
    }

    return render(request, "invitation/invitation_accept.html", context)



class InvitationDetail(DetailView):
    model = Invitation
    context_object_name = "invitation"
    template_name = "invitation/invitation_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.get_object()
        accept_url = instance.accept_url
        context["accept_url"] = accept_url 
        return context
    

    def get_object(self, queryset=None):
        return Invitation.objects.get(id=self.kwargs.get('invite_id'))