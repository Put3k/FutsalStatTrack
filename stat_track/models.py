from datetime import date, datetime, time

from django import template
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import Sum
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone

from accounts.models import CustomUser as User

TEAM_CHOICES = (
    ("blue", "blue"),
    ("orange", "orange"),
    ("colors", "colors")
)


class League(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=64)
    start_date = models.DateField(default=timezone.now)


    def __str__(self):
        return self.name

    @property
    def player_count(self):
        pass

class Player(models.Model):

    first_name = models.CharField(max_length = 16)
    last_name = models.CharField(max_length = 16)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    leagues = models.ManyToManyField(League)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def get_player_total_matchdays(self):
        """
        Returns number of total matchdays played by certain player.
        """
        matchday_count = MatchDayTicket.objects.filter(player=self).count()
        return matchday_count

    def get_player_matchdays_in_league(self, league):
        """
        Returns number of total matchdays played by certain player in certain league.
        """
        matchdays_id = MatchDayTicket.objects.filter(player=self).values('matchday')
        matchday_count = MatchDay.objects.filter(pk__in=matchdays_id, league=league).count()

        return matchday_count


    @property
    def get_player_matches_played(self):
        matches_played = Stat.objects.filter(player=self).count()
        return matches_played

    def get_player_matches_played_in_league(self, league):
        matches_played = Stat.objects.filter(player=self, league=league).count()
        return matches_played


    @property
    def get_player_goals(self):
        goals_queryset = Stat.objects.filter(player=self).values_list('goals')
        total_goals = goals_queryset.aggregate(Sum('goals'))['goals__sum']
        if total_goals:
            return total_goals
        else:
            return 0

    def get_player_goals_in_league(self, league):
        goals_queryset = Stat.objects.filter(player=self, league=league).values_list('goals')
        total_goals = goals_queryset.aggregate(Sum('goals'))['goals__sum']
        if total_goals:
            return total_goals
        else:
            return 0


    def get_player_goals_in_matchday(self, matchday):
        matches_list = list(Match.objects.filter(matchday=matchday).values_list(flat=True))
        goals_queryset = Stat.objects.filter(player=self, match__in=matches_list).values_list('goals')

        total_goals = goals_queryset.aggregate(Sum('goals'))['goals__sum'] or 0

        return total_goals


    @property
    def get_player_wins(self):
        stats = Stat.objects.filter(player=self)
        wins = sum(1 for stat in stats if stat.win==True)
        return wins

    def get_player_wins_in_league(self, league):
        stats = Stat.objects.filter(player=self, league=league)
        wins = sum(1 for stat in stats if stat.win==True)
        return wins


    @property
    def get_player_win_ratio(self):
        win_count = self.get_player_wins
        draw_count = self.get_player_draws
        matches_played = self.get_player_matches_played
        if matches_played == 0:
            win_ratio = 50
        else:
            win_ratio = round(((win_count+(draw_count/3))/matches_played)*100)

        return f"{win_ratio}%"

    def get_player_win_ratio_in_league(self, league):
        win_count = self.get_player_wins_in_league(league)
        draw_count = self.get_player_draws_in_league(league)
        matches_played = self.get_player_matches_played_in_league(league)

        if not matches_played:
            win_ratio = 50
        else:
            win_ratio = round(((win_count+(draw_count/3))/matches_played)*100)
        return f"{win_ratio}%"
    

    @property
    def get_player_loses(self):
        stats = Stat.objects.filter(player=self)
        loses = 0
        for stat in stats:
            if stat.win == False:
                loses += 1
        return loses

    def get_player_loses_in_league(self, league):
        stats = Stat.objects.filter(player=self, league=league)
        loses = sum(1 for stat in stats if stat.win==False)
        return loses


    @property
    def get_player_draws(self):
        stats = Stat.objects.filter(player=self)
        draws = 0
        for stat in stats:
            if stat.win == "Draw":
                draws += 1
        return draws

    def get_player_draws_in_league(self, league):
        stats = Stat.objects.filter(player=self, league=league)
        draws = sum(1 for stat in stats if stat.win=="Draw")
        return draws


    @property
    def get_player_goals_in_match(self, match):
        goals_queryset = Stat.objects.filter(player=self, match=match).values_list('goals')
        goals_in_match = goals_queryset.aggregate(Sum('goals'))['goals__sum']
        if goals_in_match:
            return goals_in_match
        else:
            return 0

    @property
    def get_player_goals_per_match(self):
        goals_queryset = Stat.objects.filter(player=self).values_list('goals')
        total_goals = goals_queryset.aggregate(Sum('goals'))['goals__sum']
        matches_count = Stat.objects.filter(player=self).count()
        if total_goals:
            goals_per_match = round(total_goals / matches_count, 2)
            return goals_per_match
        else:
            return 0


    def get_player_goals_per_match_in_league(self, league):
        goals_queryset = Stat.objects.filter(player=self, league=league).values_list('goals')
        total_goals = goals_queryset.aggregate(Sum('goals'))['goals__sum']
        matches_count = Stat.objects.filter(player=self, league=league).count()
        if total_goals:
            goals_per_match = round(total_goals / matches_count, 2)
            return goals_per_match
        else:
            return 0


    def get_player_team_in_matchday(self, matchday):
        ticket = MatchDayTicket.objects.get(player=self, matchday=matchday)
        team = ticket.team
        return team

    @property
    def get_total_points(self):
        stats_queryset = Stat.objects.filter(player=self)
        goals_queryset = Stat.objects.filter(player=self).values_list('goals')

        wins = self.get_player_wins
        draws = self.get_player_draws
        goals = self.get_player_goals
        score = (wins*3 + draws + goals*0.5)
        return score

    def get_total_points_in_league(self, league):
        stats_queryset = Stat.objects.filter(player=self, league=league)
        goals_queryset = Stat.objects.filter(player=self, league=league).values_list('goals')

        wins = self.get_player_wins_in_league(league)
        draws = self.get_player_draws_in_league(league)
        goals = self.get_player_goals_in_league(league)
        score = (wins*3 + draws + goals*0.5)
        return score
    

    @property
    def get_points_per_match(self):
        points = self.get_total_points
        matches_played = Stat.objects.filter(player=self).count()

        if matches_played > 0:
            points_per_match = round(points/matches_played, 2)
        else:
            points_per_match = 0

        return points_per_match

    def get_points_per_match_in_league(self, league):
        points = self.get_total_points_in_league(league)
        matches_played = Stat.objects.filter(player=self, league=league).count()

        if matches_played > 0:
            points_per_match = round(points/matches_played, 2)
        else:
            points_per_match = 0

        return points_per_match


    #Check if player already exists in database
    @property
    def player_is_valid(self):
        first_name = self.first_name.capitalize()
        last_name = self.last_name.capitalize()

        player_exists = Player.objects.filter(first_name=first_name, last_name=last_name).exists()
        if player_exists:
            player = Player.objects.get(first_name=first_name, last_name=last_name)
        if player_exists and player != self:
            return False
        else:
            return True

    def clean(self):
        if not self.player_is_valid:
            raise ValidationError("Player already exists")

    #Override save method to save data with capital letters
    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        self.full_clean()
        super(Player, self).save(*args, **kwargs)

    
    class Meta:
        ordering = ['last_name']

class MatchDay(models.Model):

    league = models.ForeignKey(League, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField("Date of match", default=datetime.now, blank=True)
    match_counter = models.PositiveIntegerField(default=0, )

    def __str__(self):
        return f"Matchday {self.date.strftime('%d-%m-%Y')}"

    #Generates list of stats as string to display it as list
    @property
    def get_teams_stats_string(self):
        match_list = Match.objects.filter(matchday=self)
        stat_list = Stat.objects.filter(match__in=match_list)

        team_stats = {
            "blue":{
                "wins":0,
                "loses":0,
                "draws":0,
                "matches":0,
                "points":0
            },
            "orange":{
                "wins":0,
                "loses":0,
                "draws":0,
                "matches":0,
                "points":0
            },
            "colors":{
                "wins":0,
                "loses":0,
                "draws":0,
                "matches":0,
                "points":0
            }
        }

        for match in match_list:
            home_team = match.team_home
            away_team = match.team_away
            result = match.result

            team_stats[home_team]["matches"] += 1
            team_stats[away_team]["matches"] += 1

            if result == 0:
                team_stats[home_team]["draws"] += 1
                team_stats[home_team]["points"] += 1

                team_stats[away_team]["draws"] += 1
                team_stats[away_team]["points"] += 1

            elif result == 1:
                team_stats[home_team]["wins"] += 1
                team_stats[home_team]["points"] += 3

                team_stats[away_team]["loses"] += 1

            elif result == 2:
                team_stats[home_team]["loses"] += 1

                team_stats[away_team]["wins"] += 1
                team_stats[away_team]["points"] += 3
        
        return team_stats


        class Meta:
            ordering = ['date']

    #Returns list of player instances assigned to this matchday
    @property
    def players(self):
        tickets = MatchDayTicket.objects.filter(matchday=self)
        players = [ticket.player for ticket in tickets]
        return players

    @property
    def players_id(self):
        tickets = MatchDayTicket.objects.filter(matchday=self)
        players_ids = [ticket.player.id for ticket in tickets]
        return players_ids
        
class MatchDayTicket(models.Model):
    #Model to store data of players assigned to team in matchday

    matchday = models.ForeignKey(MatchDay, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.CharField(choices=TEAM_CHOICES, max_length=16)

    def __str__(self):
        return f"Ticket-{self.matchday.date.strftime('%d-%m-%Y')}-{self.player.id}-{self.id}"

class Match(models.Model):

    matchday = models.ForeignKey(MatchDay, on_delete=models.CASCADE, default=None)
    team_home = models.CharField(choices=TEAM_CHOICES, max_length=20)
    team_away = models.CharField(choices=TEAM_CHOICES, max_length=20)
    home_goals = models.IntegerField(default=0)
    away_goals = models.IntegerField(default=0)
    match_in_matchday = models.IntegerField(default = 0)


    @property
    def score(self):
        return f"{self.home_goals} - {self.away_goals}"

    @property
    def result(self):   
        """returns 1 for home, 2 for away, 0 for draw"""
        if self.home_goals > self.away_goals:
            return 1
        elif self.home_goals < self.away_goals:
            return 2
        else:
            return 0

    @property
    def winner_team(self):
        """returns color of winner team"""
        if self.result == 1:
            return self.team_home
        elif self.result == 2:
            return self.team_away
        else:
            return None

    @property
    def loser_team(self):
        """returns color of losing team"""
        if self.result == 1:
            return self.team_away
        elif self.result == 2:
            return self.team_home
        else:
            return None

    @property
    def print_match(self):
        return f"{self.team_home.capitalize()} {self.home_goals} - {self.away_goals} {self.team_away.capitalize()}"

    def clean(self):
        """check if team_home and team_away are different"""

        if self.team_home == self.team_away:
            raise ValidationError("Home team and Away team cannot be the same.")

        if self.home_goals < 0 or self.away_goals < 0:
            raise ValidationError("Goals scored cannot be negative.")

    def __str__(self):
        return f"{self.match_in_matchday}-{self.matchday.date.strftime('%d-%m-%Y')}-{self.team_home}-{self.team_away}"


    class Meta:
        ordering = ['matchday']

class Stat(models.Model):

    def positive_validator(value):
        """Checks if value passed to goals is positive."""
        if value < 0:
            raise ValidationError('Value of this field can not be negative.')

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    goals = models.IntegerField(validators=[positive_validator], default=0)


    def __str__(self):
        return f"ID: {self.id} - {self.match}  - {self.player.first_name} {self.player.last_name}"

    @property
    def get_team(self):
        """Get player team"""
        matchday = self.match.matchday

        ticket = MatchDayTicket.objects.filter(matchday=matchday, player=self.player).get()
        team = ticket.team
        return team

    @property
    def win(self):
        """Result of match for certain Player"""
        match_winner_team = self.match.winner_team
        if match_winner_team == self.get_team:
            return True
        elif match_winner_team == None:
            return "Draw"
        else:
            return False

    #Validation Functions
    @property
    def player_is_valid(self):
        """Check if Player already exists in match."""

        players = Stat.objects.filter(match=self.match).values_list('player', flat=True)
        if self.player.id in players:
            return False
        else:
            return True

    #NOT IN USE DUE TO TEAM_GOALS SUM UP AS GOALS SCORED BY PLAYERS
    # @property
    # def goals_is_valid(self):
    #     """Chceck if goals scored by player and other teammates sum up to goals declared in Match."""

    #     #set value of goals scored by team
    #     if self.get_team == self.match.team_home:
    #         goals_scored_by_team = self.match.home_goals
    #     else:
    #         goals_scored_by_team = self.match.away_goals

    #     matchday = self.match.matchday
    #     teammates_queryset = MatchDayTicket.objects.filter(matchday = matchday, team = self.get_team).values('player_id')
    #     teammates = [Player.objects.get(pk=value['player_id']) for value in teammates_queryset]
    #     goals_scored_by_teammates = 0

    #     for player in teammates:
    #         player_goals = player.get_player_goals_in_match(match = self.match)
    #         if player_goals != None:
    #             goals_scored_by_teammates += player_goals

    #     if self.goals > goals_scored_by_team - goals_scored_by_teammates:
    #         return False
    #     else:
    #         return True


    @property
    def team_is_valid(self):
        """Check if team assigned to player in stat appears in match."""

        if self.get_team != self.match.team_home and self.get_team != self.match.team_away:
            return False
        else:
            return True

    def save(self, *args, **kwargs):
        if not self.league:
            self.league = self.match.matchday.league
        super(Stat, self).save(*args, **kwargs)

    def clean(self):
        #Player validation
        if not self.player_is_valid:
            raise ValidationError(f'Stat for {self.player} in this match already exists.', code="invalid_player")

        #Goals validation
        # if not self.goals_is_valid:
        #     raise ValidationError(f'Sum of the goals of the individual players is not equal the declared match goals - {self.player}', code="invalid_goal")

        if not admin.site.is_registered(self.__class__):
        #Team exists in match validation
            if not self.team_is_valid:
                raise ValidationError(f'Team {self.get_team} does not appear in this match.', code="invalid_team")


@receiver(post_save, sender=Match)
def increment_match_counter(sender, instance, created, **kwargs):
    """
    Increment match counter in Matchday after creation of Match and set its number.
    """
    if created:
        matchday = instance.matchday
        if matchday:
            matchday.match_counter += 1
            matchday.save()
        
        instance.match_in_matchday = matchday.match_counter
        instance.save()

@receiver(post_delete, sender=Match)
def decrement_match_counter(sender, instance, **kwargs):
    """
    Decrement match counter in Matchday after deletion of Match.
    """
    matchday = instance.matchday
    match_in_matchday = instance.match_in_matchday
    if matchday:
        matchday.match_counter -= 1
        matchday.save()

    with transaction.atomic():
        # Get all Match records in certain MatchDay, which match_in_matchday is greater than deleted value.
        matches_to_decrement = Match.objects.filter(matchday=matchday, match_in_matchday__gt=match_in_matchday)

        # Decrement match_in_matchday in all found records.
        matches_to_decrement.update(match_in_matchday=models.F('match_in_matchday') - 1)