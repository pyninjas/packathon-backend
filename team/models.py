from django.db import models
from project.models import Project


class Team(models.Model):
    """
    Model for Teams
    """
    name = models.CharField(max_length=255, blank=False, null=False)
    project = models.OneToOneField(Project, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
