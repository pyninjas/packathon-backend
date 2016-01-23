from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import localtime, now
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from project.serializers import ProjectSerializer
from project.models import Project
from team.models import Team
from common.models import Settings


class ProjectViewSet(viewsets.ModelViewSet):
    """
    View for Project

    **Vote:**
    /api/projects/<id>/vote

    *Vote Responses:*
        * 409: Vote not started yet
        * 409: Vote ended
        * 404: Project does not exists
        * 404: No team assigned to project
        * 400: You cannot vote for your own project
        * 400: Already voted for this project
        * 200: Vote Accepted
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_fields = ('name', 'team')

    @detail_route(methods=['post'], permission_classes=[IsAuthenticated])
    def vote(self, request, pk=None):
        """
        Additional call for voting to project
        :param request: Django Request
        :param pk: Project id
        :return: json
        """
        project_settings = Settings.objects.all()[0]
        if localtime(now()) < project_settings.vote_start_time:
            return Response({'status': False, 'message': _('Vote not started yet')}, 409)
        if localtime(now()) > project_settings.vote_end_time:
            return Response({'status': False, 'message': _('Vote ended')}, 409)
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({'status': False, 'message': _('Project does not exists')}, 404)
        try:
            team = Team.objects.get(project=project)
        except Team.DoesNotExist:
            return Response({'status': False, 'message': _('No team assigned to project')}, 404)
        if request.user.team == team:
            return Response({'status': False, 'message': _('You cannot vote for your own project')}, 400)
        if request.user.voted_for:
            if request.user.voted_for == project:
                # User already voted for this project
                return Response({'status': False, 'message': _('Already voted for this project')}, 400)
            # User is changing his vote
            unlucky_project = request.user.voted_for
            unlucky_project.votes -= 1
            unlucky_project.save()
        project.votes += 1
        request.user.voted_for = project
        project.save()
        request.user.save()
        return Response({'status': True, 'message': _('Vote Accepted')})
