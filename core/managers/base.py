import random

from django.contrib.gis.db import models

from core.querysets.base import BaseQuerySet


class BaseManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self._alive_only = kwargs.pop('alive_only', True)
        super(BaseManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self._alive_only:
            return BaseQuerySet(self.model).alive()
        return BaseQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()

    def random(self):
        return random.choice(self.all())
