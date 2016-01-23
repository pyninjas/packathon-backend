from django.utils.translation import ugettext, ugettext_lazy as _
from django.db import models


class Project(models.Model):
    """
    Model for Projects
    """
    name = models.CharField(max_length=255, blank=False, null=False)
    git = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name
