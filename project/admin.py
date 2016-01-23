from django.contrib import admin
from project.models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'votes',)

admin.site.register(Project, ProjectAdmin)
