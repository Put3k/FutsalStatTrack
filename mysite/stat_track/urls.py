from django.urls import path

from . import views

urlpatterns = [
    #HTML Views
    path("", views.home, name="home"),
    # path("league", views.league_home, name="leagues_home"),
    # path("league/<int:league_id>/", views.league_view, name="league_name"),
    path('player/<int:player_id>/', views.player_stats, name="player_stats"),
    path('players_list/', views.players_list, name="players_list" ),
    path('league/<int:league_id>/', views.league_home, name="league_home"),
    path('league/create/', views.create_league, name="create_league"),
    path('matchday/<int:matchday_id>/', views.matchday, name="matchday"),
    path('matchday/create/', views.match_creator_matchday, name="create_matchday"),
    path('matchday/<int:matchday_id>/edit', views.edit_matchday, name="edit_matchday"),
    path('delete_match/<int:match_id>/', views.delete_match, name="delete_match"),
    
    #AJAX Data Views
    path('ajax_load_players/', views.load_players, name='ajax_load_players'), #AJAX

]