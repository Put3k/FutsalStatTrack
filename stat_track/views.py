import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import is_league_member_or_owner, is_league_owner
from .forms import LeagueForm, MatchCreator, MatchDayForm, PlayerForm
from .models import League, Match, MatchDay, MatchDayTicket, Player, Stat, PlayerStatSum
from .expressions import winrate_expression, goals_per_match_expression, points_per_match_expression


def home(request):
    user_owned_leagues = []
    player_leagues = []
    player = None


    if not request.user.is_authenticated:
        context = {
            "user_owned_leagues": user_owned_leagues,
            "player_leagues": player_leagues,}
        return render(request, "home.html", context)

    user = request.user
    try:
        player = Player.objects.get(user=user)
    except:
        raise ValueError(f"User {user} have no Player assigned.")

    # leagues querysets
    user_owned_leagues = League.objects.filter(owner=user)
    player_leagues = player.leagues.all()

    # leagues counts
    owned_count = user_owned_leagues.count()
    member_count = player_leagues.count()
    
    #Manage route depending on user leagues
    if owned_count == 0 and member_count == 0:
        return redirect("league_create")
    
    elif owned_count == 1 and member_count == 0:
        return redirect("league_home", user_owned_leagues.first().pk)

    elif owned_count == 0 and member_count == 1:
        return redirect("league_home", player_leagues.first().pk)
    
    elif owned_count == 1 and member_count == 1 and user_owned_leagues.first() == player_leagues.first():
        return redirect("league_home", player_leagues.first().pk)

    context = {
        "user_owned_leagues": user_owned_leagues,
        "player_leagues": player_leagues,}

    return render(request, "home.html", context)


@login_required
@is_league_member_or_owner
def league_home(request, league_id):
    league = get_object_or_404(League, pk=league_id)
    owner = league.owner

    latest_match_day_list = MatchDay.objects.filter(league=league).order_by("-date")[:6]

    #top 5 scorers list
    players_stat_sum_qs = PlayerStatSum.objects.filter(league=league).values(
        'player', 'player__first_name', 'player__last_name', 'goals', 'match_count',
        'wins', 'points', 'draws').order_by('-goals')[:5]

    for item in players_stat_sum_qs:
        if item['match_count'] == 0:
            winrate = 50
        else:
            winrate = round(((item['wins'] + (item['draws'] / 3)) / item['match_count']) * 100)

        item['winrate'] = f"{winrate}%"


    context = {
        "latest_match_day_list": latest_match_day_list,
        "players_stat_sum_list": players_stat_sum_qs,
        "league": league,
        "owner": owner
        }
    return render(request, "league_home.html", context)

@login_required
def create_league(request):

    form = LeagueForm()

    if request.method == "POST":
        form = LeagueForm(request.POST)
        if form.is_valid():
            league = form.save(commit=False)
            league.owner = request.user
            league.save()
            league_name = league.name
            league_id = league.id

            if form.cleaned_data.get("add_owner"):
                player = request.user.players.first()
                player.leagues.add(league)

            messages.success(request, f"{league_name} created successfully.")
            return redirect(f'/league/{league_id}/')

    else:
        form = LeagueForm(request.POST)

    context = {
        'form': form,
    }

    return render(request, "league_create.html", context)


@login_required
@is_league_member_or_owner
def player_stats(request, player_id, league_id):
    league = get_object_or_404(League, pk=league_id)
    player = get_object_or_404(Player, pk=player_id)
    return render(request, "player.html", {"player": player})

@login_required
@is_league_member_or_owner
def players_list(request, league_id):
    league = League.objects.get(pk=league_id)

    players_stat_sum_list = PlayerStatSum.objects.filter(league=league).select_related('player').annotate(
        winrate=winrate_expression,
        goals_per_match=goals_per_match_expression,
        points_per_match=points_per_match_expression,
    )

    context = {
        "league": league,
        "players_stats_sum_list": players_stat_sum_list,
    }

    return render(request, "players_list.html", context)

@login_required
@is_league_member_or_owner
def matchday(request, matchday_id):
    matchday = MatchDay.objects.get(pk=matchday_id)
    matches_in_matchday_list = Match.objects.filter(matchday=matchday_id)
    league = matchday.league
    owner = league.owner

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
        "league": league,
        "owner": owner,
        "tickets": tickets,
        "team_blue": team_blue,
        "team_orange": team_orange,
        "team_colors": team_colors,
        "blue_stats": blue_stats,
        "orange_stats": orange_stats,
        "colors_stats": colors_stats,
        }

    return render(request, "matchday.html", context)

@login_required
@is_league_owner
def matchday_delete(request, matchday_id):
    matchday = get_object_or_404(MatchDay, id=matchday_id)
    league_id = matchday.league.id

    if request.method == "POST":
        decision = request.POST["action"]
        if decision == "delete":
            matchday.delete()
            messages.success(request, "Matchday deleted successfully.")
            return redirect(f'league_home', league_id)
        elif decision == "cancel":
            return redirect(f'matchday', matchday.id)
    
    context = {
        "matchday": matchday,
        "league_id": league_id,
    }
    return render(request, "matchday_delete.html", context)

@login_required
@is_league_owner
@transaction.atomic
def match_creator_matchday(request, league_id):

    def create_matchday_tickets(list_of_players, matchday, team):
        """Create MatchDayTicket to assign players to teams in certain matchday."""

        for player_id in list_of_players:
            player = Player.objects.filter(pk=player_id).get()
            ticket = MatchDayTicket(matchday=matchday, player=player, team=team)
            ticket.save()

    league = get_object_or_404(League, pk=league_id)
    list_of_players = Player.objects.filter(leagues=league).order_by("last_name")
    player_form = PlayerForm()
    
    if request.method == "POST":

        #Get players sorted by teams.
        team_blue = request.POST.getlist("team_blue")
        team_orange = request.POST.getlist("team_orange")
        team_colors = request.POST.getlist("team_colors")

        if "saveMatchday" in request.POST:
            blue_empty = len(team_blue) == 0
            orange_empty = len(team_orange) == 0
            colors_empty = len(team_colors) == 0

            #Check if at least 2 teams are populated
            if blue_empty + orange_empty + colors_empty > 1:
                messages.error(request, "There must be at least 2 teams populated!")

                form = MatchDayForm(request.POST)

                context = {
                    "league": league,
                    "list_of_players": list_of_players,
                    "form": form,
                    "player_form": player_form,
                    "team_blue": team_blue,
                    "team_orange": team_orange,
                    "team_colors": team_colors
                }
                return render(request, "create_matchday.html", context)

            #Save MatchDay form and access instance of it.
            form = MatchDayForm(request.POST)
            if form.is_valid():
                
                #get date data
                date = form.cleaned_data['date']

                #change datetime to 21:00
                modified_date = datetime.datetime(date.year, date.month, date.day, 21, 0, 0)

                matchday = form.save()
                matchday.league = league
                matchday.date = modified_date
                matchday.save()

                create_matchday_tickets(team_blue, matchday, "blue")
                create_matchday_tickets(team_orange, matchday, "orange")
                create_matchday_tickets(team_colors, matchday, "colors")

                return redirect(f"/matchday/{matchday.id}/edit")
            
            else:
                messages.error(request, "Date of matchday is required!")

        elif "addPlayer" in request.POST:

            form = MatchDayForm(request.POST)
            player_form = PlayerForm(request.POST)
            if player_form.is_valid():
                player = player_form.save()
                player.leagues.add(league)

    else:
        team_blue = None
        team_orange = None
        team_colors = None
        form = MatchDayForm()
    
    player_form = PlayerForm()

    context = {
        "league": league,
        "list_of_players": list_of_players,
        "form": form,
        "player_form": player_form,
        "team_blue": team_blue,
        "team_orange": team_orange,
        "team_colors": team_colors
    }

    return render(request, "create_matchday.html", context)

@login_required
@is_league_owner
def edit_matchday(request, matchday_id):

    #get matchday
    matchday = get_object_or_404(MatchDay, pk=matchday_id)
    league = matchday.league

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

        stat_counter = 0

        try:
            with transaction.atomic():
                match.full_clean()  # Validate match data
                match.save()

                for key, value in request.POST.items():
                    
                    if len(key)==36 and value.isdigit():
                        stat_counter += 1
                        goals = value
                        player = Player.objects.get(pk=key)
                        stat = Stat(player=player, match=match, goals=goals, league=league)
                        
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

    #get teams participating in matchday
    team_colors = {}
    for ticket in ticket_list:
        color = ticket.team.lower()
        team_colors[color] = team_colors.get(color, 0) + 1
    teams = [color for color, count in team_colors.items() if count > 0]

    form = MatchCreator()

    context = {
        "league":league,
        "match_list":match_list,
        "matchday":matchday,
        "ticket_list":ticket_list,
        "teams":teams,
        "form":form,
        }

    return render(request, "edit_matchday.html", context)

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

        template_home = "players_home_dropdown_list_options.html"
        return render(request, template_home, context_home)
        # data["home_data"] = home_data

    if team == "away":

        team_color = request.GET.get('team_away')
        players_away_id_list = MatchDayTicket.objects.filter(matchday=matchday, team=team_color).values_list("player", flat=True)
        players_away = Player.objects.filter(pk__in=players_away_id_list)
        context_away = {"players_away":players_away}
        template_away = "players_away_dropdown_list_options.html"

        return render(request, template_away, context_away)