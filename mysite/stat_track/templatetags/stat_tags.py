from django import template

register = template.Library()

from ..models import Player

@register.simple_tag
def get_player_matchdays_in_league(player, league):
    return player.get_player_matchdays_in_league(league)


@register.simple_tag
def get_player_goals_in_matchday(player, matchday):
    return player.get_player_goals_in_matchday(matchday)

