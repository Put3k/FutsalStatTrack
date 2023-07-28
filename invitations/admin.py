from django.contrib import admin

from .models import Invitation


class InvitationAdmin(admin.ModelAdmin):
    readonly_fields = ('id', )

admin.site.register(Invitation, InvitationAdmin)
