import datetime
from django.db import models
from django.db.models import Q


class ActivityQuerySet(models.QuerySet):
    """ Activity QuerySet"""

    def active_activities(self):
        """ Active activities """
        return self.filter(is_active=True)

    def date(
        self,
        start: datetime.date,
        end: datetime.date = None
    ):
        """ Activities by start and end dates """
        query = Q(start__gte=start)
        if end:
            query.add(
                Q(start__lte=end), Q.AND
            )
        return self.filter(query)


class ActivityManager(models.Manager):
    """ Activity Manager"""

    def get_queryset(self):
        return ActivityQuerySet(self.model, using=self._db)

    def get_coming_activities(self):
        today = datetime.date.today()
        return self.get_queryset().active_activities().date(today)
