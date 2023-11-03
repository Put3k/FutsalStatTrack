from django.contrib import admin
from django.db import transaction
from django.db.models import Sum
from .models import PlayerStatSum

@admin.action(description="Summarize player stats")
def summarize_player_stats(modeladmin, request, queryset):

    queryset = queryset.prefetch_related(
        'leagues',
        'playerstatsum_set',
        'stat_set__match',
        'matchdayticket_set',
    )

    with transaction.atomic():

        for player in queryset:
            if not player.playerstatsum_set.exists():
                for league in player.leagues.all():
                    existing_player_stat_sum = player.playerstatsum_set.filter(league=league).first()

                    if not existing_player_stat_sum:
                        player_stat_sum = PlayerStatSum(player=player, league=league)
                    else:
                        player_stat_sum = existing_player_stat_sum

                    player_stat_sum.goals = player.stat_set.filter(league=league).aggregate(Sum('goals'))['goals__sum'] or 0
                    player_stat_sum.match_count = player.stat_set.filter(league=league).count()
                    player_stat_sum.matchday_count = player.matchdayticket_set.filter(matchday__league=league).count()
                    player_stat_sum.wins = sum(1 for stat in player.stat_set.filter(league=league) if stat.win is True)
                    player_stat_sum.draws = sum(1 for stat in player.stat_set.filter(league=league) if stat.win == "Draw")
                    player_stat_sum.loses = sum(1 for stat in player.stat_set.filter(league=league) if stat.win is False)
                    player_stat_sum.points = 3 * player_stat_sum.wins + player_stat_sum.draws
                    player_stat_sum.save()

        # Populate existing PlayerStatSum instances