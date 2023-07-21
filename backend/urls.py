from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # User management
    # path('accounts/', include("django.contrib.auth.urls")),
    path("accounts/", include("allauth.urls")),

    # Local apps
    path('', include("stat_track.urls")),
    
    # API
    path('api/', include("api.urls")),
    path('api/v2/', include("backend.routers"))
]
