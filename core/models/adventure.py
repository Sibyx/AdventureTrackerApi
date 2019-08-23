import enum

from django.contrib.gis.db import models
from django_enum_choices.fields import EnumChoiceField

from core.models.base import BaseModel


class AdventureType(enum.Enum):
    DRAFT = 'DRAFT'
    PLANNED = 'PLANNED'
    IN_PROGRESS = 'IN_PROGRESS'
    FINISHED = 'FINISHED'


class Adventure(BaseModel):
    class Meta:
        app_label = 'core'
        default_permissions = ()
        db_table = 'adventures'

    status = EnumChoiceField(AdventureType)
    happened_at = models.DateTimeField()
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField(null=True, blank=True)
