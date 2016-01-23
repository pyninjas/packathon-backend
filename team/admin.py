from django.contrib import admin
from team.models import Team

class TeamAdmin(admin.ModelAdmin):
    pass
admin.site.register(Team, TeamAdmin)
