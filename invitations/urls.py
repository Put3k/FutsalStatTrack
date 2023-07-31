from django.urls import path

from . import views

urlpatterns = [

    path("create/<uuid:player_id>/", views.create_invitation, name="invitation_create"),
    path("<uuid:invite_id>/", views.InvitationDetail.as_view(), name="invitation_detail"),
    path("<str:key>/", views.accept_invitation, name="invitation_accept"),
]
