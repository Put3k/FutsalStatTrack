from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # User management
    path("accounts/", include("allauth.urls")),

    # Local apps
    path('', include("stat_track.urls")),
    
    # API
    path('api/', include("api.urls")),
    path('api/v2/', include("backend.routers"))
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns