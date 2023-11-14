from django.apps import apps
def get_player_stat_sum(player, league):
    """
    If PlayerStatSum for player and league exists, returns existing instance;
    If not, it creates new one.
    """

    stat_sum_model = apps.get_model('stat_track.PlayerStatSum')

    player_stat_sum = stat_sum_model.objects.filter(player=player, league=league)
    if player_stat_sum:
        player_stat_sum = player_stat_sum.get()
    else:
        player_stat_sum = stat_sum_model(player=player, league=league)

    return player_stat_sum
