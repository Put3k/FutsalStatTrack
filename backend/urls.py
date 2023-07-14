from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("stat_track.urls")),
    path('user/', include("django.contrib.auth.urls")),
    path('user/', include("users.urls")),
    path('api/', include("api.urls")),
    path('api/v2/', include("backend.routers"))
]
