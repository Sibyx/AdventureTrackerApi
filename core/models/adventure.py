from django.contrib.gis.db import models
from django_enumfield import enum

from core.models.base import BaseModel


class AdventureType(enum.Enum):
    DRAFT = 0
    PLANNED = 1
    IN_PROGRESS = 2
    FINISHED = 3

    labels = {
        DRAFT: 'DRAFT',
        PLANNED: 'PLANNED',
        IN_PROGRESS: 'IN_PROGRESS',
        FINISHED: 'FINISHED'
    }


class Adventure(BaseModel):
    class Meta:
        app_label = 'core'
        default_permissions = ()
        db_table = 'adventures'

    status = enum.EnumField(AdventureType)
    code = models.UUIDField(unique=True)
    happened_at = models.DateTimeField()
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField(null=True, blank=True)
