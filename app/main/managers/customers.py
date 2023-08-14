# import datetime
from django.db import models
from django.db.models import Q


class CustomerQuerySet(models.QuerySet):
    """ Customer QuerySet"""

    def active_customers(self):
        """ Active customers """
        return self.filter(is_active=True)


class CustomerManager(models.Manager):
    """ Customer Manager"""

    def get_queryset(self):
        return CustomerQuerySet(self.model, using=self._db)
