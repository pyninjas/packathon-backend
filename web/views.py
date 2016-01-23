from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.http import Http404
from django.utils import timezone
from django.conf import settings
# from rest_framework.response import Response
from common.models import Settings
from common.forms import ProfileForm
from project.models import Project
from project.forms import ProjectForm
from team.models import Team
from feed.models import Feed
import pytz


def convert_time_to_str(vote_time):
    vote_time_str = ''
    if vote_time.hour < 10:
        vote_time_str += '0' + str(vote_time.hour)
    else:
        vote_time_str += str(vote_time.hour)
    vote_time_str += ':'
    if vote_time.minute < 10:
        vote_time_str += '0' + str(vote_time.minute)
    else:
        vote_time_str += str(vote_time.minute)
    return vote_time_str


def get_user(email):
    try:
        return get_user_model().objects.get(email=email.lower())
    except get_user_model().DoesNotExist:
        return None


def login_view(request):
    """
    Custom login for users using email
    :param request: Django Request
    :return: Rendered HTML
    """
    data = {'error': None}
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        next_url = request.POST['next']
        if not email or not password:
            return render(request, 'web/login.html', {'error': _('Missing Fields')})
        username = get_user(email)
        if not username:
            return render(request, 'web/login.html', {'error': _('User not found')})
        username = username.username
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(next_url)
            else:
                return render(request, 'web/login.html', {'error': _('Account Disabled')})
        else:
            return render(request, 'web/login.html', {'error': _('Invalid login details')})
    return render(request, 'web/login.html', data)


def index(request):
    """
    Home page
    :param request: Django request
    :return: Rendered HTML
    """
    project_settings = Settings.objects.all()[0]
    local_time = timezone.localtime(timezone.now())
    vote_time = project_settings.vote_start_time.astimezone(
        pytz.timezone(getattr(settings, "TIME_ZONE", 'Asia/Baku')))

    end_time = project_settings.vote_end_time.astimezone(
        pytz.timezone(getattr(settings, "TIME_ZONE", 'Asia/Baku')))

    vote_start_str = convert_time_to_str(vote_time)
    vote_end_str = convert_time_to_str(end_time)

    data = {
        'vote_time': vote_start_str,
        'vote_left': int((vote_time - local_time).total_seconds()),
        'end_time': vote_end_str,
        'end_left': int((end_time - local_time).total_seconds())
    }
    return render(request, 'web/index.html', data)


def projects(request, pk=None):
    """
    Project list (if pk=None) or single project
    :param request: Django request
    :param pk: Project id
    :return: Rendered HTML
    """
    project = None
    project_list = None
    if pk:
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404(_('Project not found'))
    else:
        project_list = Project.objects.all()
    if pk:
        try:
            team = Team.objects.get(project=project)
        except Team.DoesNotExist:
            raise Http404(_('Team not set'))
        try:
            users = get_user_model().objects.filter(team=team)
        except get_user_model().DoesNotExist:
            raise Http404(_('No users attached to team'))
        data = {
            'project': project,
            'team': team,
            'users': users
        }
        return render(request, 'web/project.html', data)
    data = {
        'projects': project_list
    }
    return render(request, 'web/projects.html', data)


def teams(request, pk=None):
    """
    Team list (if pk=None) or single team
    :param request: Django Request
    :param pk: Team id
    :return: Rendered HTML
    """
    team = None
    team_list = None
    if pk:
        try:
            team = Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            raise Http404(_('Team not found'))
    else:
        # team_list = Team.objects.filter(project__isnull=False)
        team_list = Team.objects.all()
    if pk:
        try:
            users = get_user_model().objects.filter(team=team)
        except get_user_model().DoesNotExist:
            raise Http404(_('No users attached to team'))
        data = {
            'team': team,
            'users': users
        }
        if not team.project:
            data['project'] = {'name': _('Packathon')}
            data['website'] = '/'
        else:
            data['project'] = team.project
            data['website'] = team.project.website
        return render(request, 'web/team.html', data)
    data = {
        'teams': team_list
    }
    return render(request, 'web/teams.html', data)


def feed(request):
    """
    Feed view
    :param request: Django Request
    :return: Rendered HTML
    """
    feed_list = Feed.objects.all().order_by('-id')
    data = {
        'feed': feed_list
    }
    return render(request, 'web/feed.html', data)


def profile(request, pk=None):
    """
    Preview and edit profile page
    :param request: Django Request
    :param pk: user id
    :return: Rendered HTML
    """
    if not request.user.is_authenticated():
        return redirect('/')
    if request.user.pk != int(pk):
        return redirect('user-profile', pk=request.user.pk)
    if request.method == 'POST':
        # handle post
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save(commit=True)
            return redirect('user-profile', pk=request.user.pk)
        return render(request, 'web/profile.html', {'form': form})
    # get request
    form = ProfileForm(instance=request.user)
    data = {
        'form': form,
        'user': request.user
    }
    return render(request, 'web/profile.html', data)


def add_project(request):
    """
    Add project for own team
    :param request: Django Request
    :return: Rendered HTML
    """
    if not request.user.is_authenticated():
        return redirect('/')
    if not request.user.team:
        return redirect('/')
    project = request.user.team.project
    if request.method == 'POST':
        # handle post
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save(commit=True)
            team = request.user.team
            team.project = project
            team.save()
            return redirect('project-view', pk=project.pk)
    form = ProjectForm(instance=project)
    data = {
        'form': form,
        'user': request.user,
        'error': None
    }
    return render(request, 'web/add_project.html', data)
