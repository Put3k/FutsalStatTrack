from django.urls import path

from . import views

urlpatterns = [
    #HTML Views
    path("", views.home, name="home"),

    path('league/<uuid:league_id>/player/<uuid:player_id>/', views.player_stats, name="player_stats"),

    path('league/<uuid:league_id>/', views.league_home, name="league_home"),
    path('league/create/', views.create_league, name="league_create"),
    path('league/<uuid:league_id>/players_list/', views.players_list, name="players_list" ),
    path('league/<uuid:league_id>/create_matchday/', views.match_creator_matchday, name="matchday_create"),

    path('matchday/<uuid:matchday_id>/', views.matchday, name="matchday"),
    path('matchday/<uuid:matchday_id>/edit', views.edit_matchday, name="matchday_edit"),
    path('matchday/<uuid:matchday_id>/delete', views.matchday_delete, name="matchday_delete"),

    path('delete_match/<uuid:match_id>/', views.delete_match, name="delete_match"),
    
    #AJAX Data Views
    path('ajax_load_players/', views.load_players, name='ajax_load_players'), #AJAX

]