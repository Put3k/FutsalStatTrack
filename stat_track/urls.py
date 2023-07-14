from django.urls import path

from . import views

urlpatterns = [
    #HTML Views
    path("", views.home, name="home"),

    path('league/<int:league_id>/player/<int:player_id>/', views.player_stats, name="player_stats"),

    path('league/<int:league_id>/', views.league_home, name="league_home"),
    path('league/<int:league_id>/players_list/', views.players_list, name="players_list" ),
    path('league/<int:league_id>/create_matchday/', views.match_creator_matchday, name="matchday_create"),
    path('league/create/', views.create_league, name="league_create"),

    path('matchday/<int:matchday_id>/', views.matchday, name="matchday"),
    path('matchday/<int:matchday_id>/edit', views.edit_matchday, name="matchday_edit"),
    path('matchday/<int:matchday_id>/delete', views.matchday_delete, name="matchday_delete"),

    path('delete_match/<int:match_id>/', views.delete_match, name="delete_match"),
    
    #AJAX Data Views
    path('ajax_load_players/', views.load_players, name='ajax_load_players'), #AJAX

]