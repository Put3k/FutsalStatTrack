from django.contrib import admin
from django import forms
from .models import Match, MatchDay, MatchDayTicket, Player, Stat, League

class LeagueAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'owner')

class MatchDayAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'match_counter')
    readonly_fields = ('match_counter', )

class MatchDayTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'matchday_id', 'player', 'team')

class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__')
    readonly_fields = ('match_in_matchday',)
    list_display_links = ('id', '__str__')

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'get_player_matches_played', 'get_player_goals', 'get_player_wins', 'get_player_loses', 'get_player_draws')


# class StatAdmin(admin.ModelAdmin):
#     def clean_fields(self, request, obj):
#         if self.model_admin:


admin.site.register(League, LeagueAdmin)
admin.site.register(MatchDay, MatchDayAdmin)
admin.site.register(MatchDayTicket, MatchDayTicketAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Stat)
