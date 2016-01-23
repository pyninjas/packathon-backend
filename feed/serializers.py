from rest_framework import serializers
from feed.models import Feed


class FeedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Feed
        fields = ('id', 'title', 'description', 'created_at')
