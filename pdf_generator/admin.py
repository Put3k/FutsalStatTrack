from django.contrib import admin

from .models import Report


class ReportAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'owner', 'league')

admin.site.register(Report, ReportAdmin)
