from django.db import models


class BaseModel(models.Model):
    """ Base Model """
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        """Meta option."""

        abstract = True
        get_latest_by = 'created'
        ordering = ['-created', '-modified']