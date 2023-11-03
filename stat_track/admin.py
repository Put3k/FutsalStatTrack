from django.contrib import admin

from .models import League, Match, MatchDay, MatchDayTicket, Player, Stat, PlayerStatSum
from .actions import summarize_player_stats


# ModelAdmin
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'owner')


class MatchDayAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'match_counter')
    readonly_fields = ('match_counter', )


class MatchDayTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'matchday', 'player', 'team')
    list_filter = ('matchday__league', 'matchday', 'player')


class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__')
    readonly_fields = ('match_in_matchday',)
    list_display_links = ('id', '__str__')
    ordering = ('matchday',)
    list_filter = ('matchday__league',)


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'user')
    actions = [summarize_player_stats]
    list_filter = ('leagues',)


class StatAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'league')
    list_filter = ('player', 'league')


class PlayerStatSumAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id')
    readonly_fields = ('goals', 'match_count', 'matchday_count', 'points', 'wins', 'loses', 'draws')


admin.site.register(League, LeagueAdmin)
admin.site.register(MatchDay, MatchDayAdmin)
admin.site.register(MatchDayTicket, MatchDayTicketAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Stat, StatAdmin)
admin.site.register(PlayerStatSum, PlayerStatSumAdmin)
