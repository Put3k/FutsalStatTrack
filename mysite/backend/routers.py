from rest_framework.routers import DefaultRouter

from stat_track.viewsets import PlayerViewSet


router = DefaultRouter()
router.register('players', PlayerViewSet, basename='players')

urlpatterns = router.urls