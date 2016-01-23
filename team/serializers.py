from rest_framework import serializers
from team.models import Team
from django.contrib.auth import get_user_model


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    users = serializers.SerializerMethodField('get_members')

    @staticmethod
    def get_members(obj):
        return get_user_model().objects.filter(team=obj).values(
            'id', 'username', 'name', 'description', 'website',
            'git', 'twitter', 'email')

    class Meta:
        model = Team
        fields = ('id', 'name', 'project', 'users')
