from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser
from team.models import Team
from project.models import Project
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination


class Hacker(AbstractUser):
    """
    Custom User object with more details
    """
    name = models.CharField(max_length=255)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)
    voted_for = models.ForeignKey(Project, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    git = models.URLField(max_length=255, blank=True, null=True)
    twitter = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.username


class AuthenticationMethod(SessionAuthentication):
    """
    Ignore CSRF for enabling Token access to api
    """
    def enforce_csrf(self, request):
        # Do not check csrf to be able to login both over web and api
        return


class ApiPagination(PageNumberPagination):
    """
    Pagination params for list results in api
    """
    page_size = 100
    page_size_query_param = 'page_size'


class Settings(models.Model):
    """
    Simple Module for storing dynamic settings variables as plugins are buggy
    """
    vote_start_time = models.DateTimeField(auto_now=False, blank=False, null=False)
    vote_end_time = models.DateTimeField(auto_now=False, blank=False, null=False)

    class Meta:
        verbose_name = _("Setting")
        verbose_name_plural = _("Settings")
