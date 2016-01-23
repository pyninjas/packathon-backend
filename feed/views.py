from rest_framework import viewsets
from feed.models import Feed
from feed.serializers import FeedSerializer


class FeedViewSet(viewsets.ModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    filter_fields = ('title', 'description', 'created_at')
