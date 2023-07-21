from django import template

register = template.Library()

from ..models import Player

@register.simple_tag
def get_player_matchdays_in_league(player, league):
    return player.get_player_matchdays_in_league(league)


@register.simple_tag
def get_player_matches_played_in_league(player, league):
    return player.get_player_matches_played_in_league(league)


@register.simple_tag
def get_player_goals_in_league(player, league):
    return player.get_player_goals_in_league(league)


@register.simple_tag
def get_player_goals_in_matchday(player, matchday):
    return player.get_player_goals_in_matchday(matchday)


@register.simple_tag
def get_player_goals_per_match_in_league(player, league):
    return player.get_player_goals_per_match_in_league(league)


@register.simple_tag
def get_player_wins_in_league(player, league):
    return player.get_player_wins_in_league(league)


@register.simple_tag
def get_player_loses_in_league(player, league):
    return player.get_player_loses_in_league(league)


@register.simple_tag
def get_player_draws_in_league(player, league):
    return player.get_player_draws_in_league(league)


@register.simple_tag
def get_player_win_ratio_in_league(player, league):
    return player.get_player_win_ratio_in_league(league)


@register.simple_tag
def get_total_points_in_league(player, league):
    return player.get_total_points_in_league(league)


@register.simple_tag
def get_points_per_match_in_league(player, league):
    return player.get_points_per_match_in_league(league)




