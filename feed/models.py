from django.db import models
from common.utils.parse import pusher


class Feed(models.Model):
    """
    Simple feed for push announcements
    """
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.title:
            pusher.send(self.title)
        super(Feed, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-created_at',)
