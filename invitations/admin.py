from django.contrib import admin

from .models import Invitation


class InvitationAdmin(admin.ModelAdmin):
    list_display = ("id", "accepted", "created", "inviter", "player", "league", "expired", "is_active")
    readonly_fields = ('id', )

admin.site.register(Invitation, InvitationAdmin)
