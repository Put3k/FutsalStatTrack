from django import template

register = template.Library()

from ..models import Player

@register.simple_tag
def get_player_goals_in_matchday(player, matchday):
    return player.get_player_goals_in_matchday(matchday)