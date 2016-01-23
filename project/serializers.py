from rest_framework import serializers
from project.models import Project
from team.models import Team


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    team = serializers.SerializerMethodField('get_project_team')

    @staticmethod
    def get_project_team(obj):
        teams = Team.objects.filter(project=obj).values('id', 'name')
        if len(teams):
            # only 1 team allowed in structure:
            return teams[0]
        return None

    class Meta:
        model = Project
        fields = ('id', 'name', 'git', 'website', 'team')
