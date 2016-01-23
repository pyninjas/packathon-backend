from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from team.models import Team
from team.serializers import TeamSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import detail_route
from django.contrib.auth import get_user_model


class TeamViewSet(viewsets.ModelViewSet):
    """
    View for teams
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_fields = ('name', 'project')

    @detail_route(methods=['get'], permission_classes=[AllowAny])
    def photo(self, request, pk=None):
        try:
            team = Team.objects.get(pk=pk)
            members = get_user_model().objects.filter(team=team)
        except Team.DoesNotExist:
            members = [_('Unknown Team')]
        except get_user_model().DoesNotExist:
            members = [_('No users')]
        members = list(members)
        while len(members) < 3:
            members.append('')
        data = {'members': members}
        return render(request, 'team/team.svg', data, content_type='image/svg+xml')
