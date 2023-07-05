import datetime
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms import formset_factory
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from rest_framework import generics

from .decorators import is_league_member_or_owner
from .forms import MatchCreator, MatchDayForm, PlayerForm, StatForm
from .models import League, Match, MatchDay, MatchDayTicket, Player, Stat
from .serializers import PlayerSerializer


def home(request):
    user_owned_leagues = []
    player_leagues = []
    player = None

    if request.user.is_authenticated:
        user = request.user
        player = Player.objects.get(user=user)

        user_owned_leagues = League.objects.filter(owner=user)
        player_leagues = player.leagues.all()

    if len(user_owned_leagues) == 1 and len(player_leagues) == 1:
        owned_league = user_owned_leagues[0]
        player_league = player_leagues[0]
        
        if owned_league==player_league:
            return redirect(f"/league/{owned_league.id}/")

    context = {
        "user_owned_leagues": user_owned_leagues,
        "player_leagues": player_leagues,
    }

    return render(request, "stat_track/home.html", context)

@login_required
@is_league_member_or_owner
def league_home(request, league_id):
    league = get_object_or_404(League, pk=league_id)
    # if not is_league_member(request.user, league):
    #     return redirect("home")

    latest_match_day_list = MatchDay.objects.order_by("-date")[:5]
    players_list = Player.objects.all()
    players_list = sorted(players_list, key=lambda x: x.get_player_goals, reverse=True)[:5]

    context = {"latest_match_day_list": latest_match_day_list, "players_list": players_list}
    return render(request, "stat_track/league_home.html", context)

# NOT IN USE
def moderator_panel(request):
    return HttpResponse("Moderator Panel")

@login_required
def player_stats(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    return render(request, "stat_track/player.html", {"player": player})

@login_required
def players_list(request):
    players_list = Player.objects.all().order_by('last_name')
    
    context = {
        "players_list": players_list
    }

    return render(request, "stat_track/players_list.html", context)

@login_required
def matchday(request, matchday_id):
    matchday = get_object_or_404(MatchDay, pk=matchday_id)
    matches_in_matchday_list = Match.objects.filter(matchday=matchday_id)

    #Assign players to teams
    tickets = MatchDayTicket.objects.filter(matchday=matchday)

    team_blue = []
    team_orange = []
    team_colors = []

    for ticket in tickets:
        if ticket.team == "blue":
            team_blue.append(ticket.player)
        elif ticket.team == "orange":
            team_orange.append(ticket.player)
        elif ticket.team == "colors":
            team_colors.append(ticket.player)

    #Present teams stats as list

    blue_stats = []
    orange_stats = []
    colors_stats = []

    team_stats = matchday.get_teams_stats_string
    for team_name, team_data in team_stats.items():
        for stat_name, stat_value in team_data.items():
            stat_entry = f"{stat_name.capitalize()}: {stat_value}"
            if team_name == "blue":
                blue_stats.append(stat_entry)
            elif team_name == "orange":
                orange_stats.append(stat_entry)
            elif team_name == "colors":
                colors_stats.append(stat_entry)

    context = {
        "matches_in_matchday_list": matches_in_matchday_list,
        "matchday": matchday,
        "tickets": tickets,
        "team_blue": team_blue,
        "team_orange": team_orange,
        "team_colors": team_colors,
        "blue_stats": blue_stats,
        "orange_stats": orange_stats,
        "colors_stats": colors_stats,
        }

    return render(request, "stat_track/matchday.html", context)

@login_required
@transaction.atomic
def match_creator_matchday(request):

    def create_matchday_tickets(list_of_players, matchday, team):
        """Create MatchDayTicket to assign players to teams in certain matchday."""

        for player_id in list_of_players:
            player = Player.objects.filter(pk=player_id).get()
            ticket = MatchDayTicket(matchday=matchday, player=player, team=team)
            ticket.save()

    list_of_players = Player.objects.all().order_by("last_name")
    form = MatchDayForm()
    player_form = PlayerForm()

    if request.method == "POST":
        if "saveMatchday" in request.POST:

            #Get players sorted by teams.
            team_blue = request.POST.getlist("team_blue")
            team_orange = request.POST.getlist("team_orange")
            team_colors = request.POST.getlist("team_colors")

            #Save MatchDay form and access instance of it.
            form = MatchDayForm(request.POST)
            if form.is_valid():
                
                #get date data
                date = form.cleaned_data['date']

                #change datetime to 21:00
                modified_date = datetime.datetime(date.year, date.month, date.day, 21, 0, 0)

                matchday = form.save()
                matchday.date = modified_date
                matchday.save()

            create_matchday_tickets(team_blue, matchday, "blue")
            create_matchday_tickets(team_orange, matchday, "orange")
            create_matchday_tickets(team_colors, matchday, "colors")

            return redirect(f"/matchday/{matchday.id}/edit")

        elif "addPlayer" in request.POST:

            form = MatchDayForm(request.POST)
            player_form = PlayerForm(request.POST)
            if player_form.is_valid():
                player = player_form.save()
    
    context = {
        "list_of_players": list_of_players,
        "form": form,
        "player_form":player_form
    }

    return render(request, "stat_track/create_matchday.html", context)


@login_required
def edit_matchday(request, matchday_id):

    #get matchday
    matchday = get_object_or_404(MatchDay, pk=matchday_id)

    if "addMatch" in request.POST:
        
        #match fields
        team_home = request.POST["team_home"]
        team_away = request.POST["team_away"]
        home_goals = request.POST.get("home_goals")
        away_goals = request.POST.get("away_goals")

        match = Match(
            matchday = matchday,
            team_home = team_home,
            team_away = team_away,
            home_goals = home_goals,
            away_goals = away_goals
        )

        stat_list = []
        stat_counter = 0

        try:
            with transaction.atomic():
                match.full_clean()  # Validate match data
                match.save()

                for key, value in request.POST.items():
                    if key.isdigit():
                        stat_counter += 1
                        player = Player.objects.filter(pk=key).first()
                        goals = value
                        stat = Stat(player=player, match=match, goals=goals)

                        stat.full_clean()  # Validate stat data
                        stat.save()

        except ValidationError as e:
            for error_message in e:
                error_str = error_message[1][0]
                messages.error(request, error_str)


    #get match list for this matchday
    match_list = Match.objects.filter(matchday=matchday)

    #get matchday tickets
    ticket_list = MatchDayTicket.objects.filter(matchday=matchday)

    form = MatchCreator()

    context = {
        "match_list":match_list,
        "matchday":matchday,
        "ticket_list":ticket_list,
        "form":form,
        }

    return render(request, "stat_track/edit_matchday.html", context)

@login_required
def delete_match(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    matchday_id = match.matchday.id
    match.delete()
    return redirect(f'/matchday/{matchday_id}/edit')


# AJAX to load players
def load_players(request):
    matchday_id = request.GET.get('matchday_id')
    matchday = MatchDay.objects.get(pk=matchday_id)

    team = request.GET.get('team')

    home_data = None
    away_data = None

    data = {}

    if team == "home":

        team_color = request.GET.get('team_home')
        players_home_id_list = MatchDayTicket.objects.filter(matchday=matchday, team=team_color).values_list("player", flat=True)
        players_home = Player.objects.filter(pk__in=players_home_id_list)
        context_home = {"players_home":players_home}

        template_home = "stat_track/players_home_dropdown_list_options.html"
        return render(request, template_home, context_home)
        # data["home_data"] = home_data

    if team == "away":

        team_color = request.GET.get('team_away')
        players_away_id_list = MatchDayTicket.objects.filter(matchday=matchday, team=team_color).values_list("player", flat=True)
        players_away = Player.objects.filter(pk__in=players_away_id_list)
        context_away = {"players_away":players_away}
        template_away = "stat_track/players_away_dropdown_list_options.html"

        return render(request, template_away, context_away)