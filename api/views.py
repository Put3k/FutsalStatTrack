import json

from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response

from stat_track.models import Match, MatchDay, MatchDayTicket, Player
from stat_track.serializers import (MatchDaySerializer, MatchSerializer,
                                    PlayerSerializer)

from .mixins import StaffEditorPermissionMixin


@api_view(["POST"])
def api_home(request, *args, **kwargs):
    """
    DRF API View
    """
    data = request.data
    serializer = PlayerSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        return Response(serializer.data)



"""
PLAYER API VIEWS
"""
class PlayerListCreateAPIView(
    StaffEditorPermissionMixin,
    generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    
player_list_create_view = PlayerListCreateAPIView.as_view()


class PlayerDetailAPIView(
    StaffEditorPermissionMixin,
    generics.RetrieveAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

player_detail_view = PlayerDetailAPIView.as_view()


class PlayerUpdateAPIView(
    StaffEditorPermissionMixin,
    generics.UpdateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    lookup_field = 'id'

    def perform_update(self, serializer):
        instance = serializer.save()

player_update_view = PlayerUpdateAPIView.as_view()


class PlayerDestroyAPIView(
    StaffEditorPermissionMixin,
    generics.DestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    lookup_field = 'id'

    def perform_destroy(self, instance):
        super().perform_destroy(instance)

player_delete_view = PlayerDestroyAPIView.as_view()


"""
MATCH API VIEWS
"""
class MatchListCreateAPIView(
    StaffEditorPermissionMixin,
    generics.ListCreateAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    
match_list_create_view = MatchListCreateAPIView.as_view()


class MatchDetailAPIView(
    StaffEditorPermissionMixin,
    generics.RetrieveAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

match_detail_view = MatchDetailAPIView.as_view()


class MatchUpdateAPIView(
    StaffEditorPermissionMixin,
    generics.UpdateAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    lookup_field = 'id'

    def perform_update(self, serializer):
        instance = serializer.save()

match_update_view = MatchUpdateAPIView.as_view()


class MatchDestroyAPIView(
    StaffEditorPermissionMixin,
    generics.DestroyAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    lookup_field = 'id'

    def perform_destroy(self, instance):
        super().perform_destroy(instance)

match_delete_view = MatchDestroyAPIView.as_view()



"""
MATCHDAY API VIEWS
"""
class MatchDayCreateAPIView(
    StaffEditorPermissionMixin,
    generics.CreateAPIView):
    queryset = MatchDay.objects.all()
    serializer_class = MatchDaySerializer
    lookup_field = 'id'

matchday_create_view = MatchDayCreateAPIView.as_view()


class MatchDayListAPIView(
    StaffEditorPermissionMixin,
    generics.ListCreateAPIView):
    queryset = MatchDay.objects.all()
    serializer_class = MatchDaySerializer
    lookup_field = 'id'

matchday_list_view = MatchDayListAPIView.as_view()


class MatchDayDetailAPIView(
    StaffEditorPermissionMixin,
    generics.RetrieveAPIView):
    queryset = MatchDay.objects.all()
    serializer_class = MatchDaySerializer

matchday_detail_view = MatchDayDetailAPIView.as_view()


class MatchDayUpdateAPIView(
    StaffEditorPermissionMixin,
    generics.UpdateAPIView):
    queryset = MatchDay.objects.all()
    serializer_class = MatchDaySerializer
    lookup_field = 'id'

    def perform_update(self, serializer):
        instance = serializer.save()

matchday_update_view = MatchDayUpdateAPIView.as_view()


class MatchDayDestroyAPIView(
    StaffEditorPermissionMixin,
    generics.DestroyAPIView):
    queryset = MatchDay.objects.all()
    serializer_class = MatchDaySerializer
    lookup_field = 'id'

    def perform_destroy(self, instance):
        super().perform_destroy(instance)

matchday_delete_view = MatchDayDestroyAPIView.as_view()



"""
M
"""