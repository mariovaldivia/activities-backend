from django.db import models
from enum import Enum


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


class ActivityStatus(Enum):
    REGISTERED = 'R'
    ACCEPTED = 'A'
    REJECTED = 'RJ'
    EXECUTING = 'E'
    DONE = 'D'

    @classmethod
    def get_value(cls, member):
        return cls[member].value[0]
