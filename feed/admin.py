from django.contrib import admin
from feed.models import Feed

class FeedAdmin(admin.ModelAdmin):
    pass
admin.site.register(Feed, FeedAdmin)
