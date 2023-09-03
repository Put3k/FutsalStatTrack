from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('', views.api_home),
    path('auth/', obtain_auth_token),
    path('players/', views.player_list_create_view, name='player-list'),
    path('players/<uuid:id>/', views.player_detail_view, name='player-detail'),
    path('players/<uuid:id>/update/', views.player_update_view, name='player-edit'),
    path('players/<uuid:id>/delete/', views.player_delete_view, name='player-delete'),

    path('matches/', views.match_list_create_view, name='match-list'),
    path('matches/<uuid:id>', views.match_detail_view, name='match-detail'),
    path('matches/<uuid:id>/update/', views.match_update_view, name='match-edit'),
    path('matches/<uuid:id>/delete/', views.match_delete_view, name='match-delete'),

    path('matchdays/create/', views.matchday_create_view, name='matchday-create'),
    path('matchdays/', views.matchday_list_view, name='matchday-list'),
    path('matchdays/<uuid:id>/', views.matchday_detail_view, name='matchday-detail'),
    path('matchdays/<uuid:id>/update/', views.matchday_update_view, name='matchday-update'),
    path('matchdays/<uuid:id>/delete/', views.matchday_delete_view, name='matchday-delete'),
]