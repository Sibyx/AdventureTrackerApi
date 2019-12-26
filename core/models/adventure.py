import enum

from django.contrib.gis.db import models
from django_enum_choices.fields import EnumChoiceField

from core.models.base import BaseModel


class AdventureStatus(enum.Enum):
    DRAFT = 'draft'
    IN_PROGRESS = 'in_progress'
    FINISHED = 'finished'


class Adventure(BaseModel):
    class Meta:
        app_label = 'core'
        default_permissions = ()
        db_table = 'adventures'

    status = EnumChoiceField(AdventureStatus)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField(null=True, blank=True)

    @property
    def summary(self) -> dict:
        response = {
            'id': self.id,
            'status': self.status,
            'name': self.name,
            'description': self.description,
            'members': self.users.values_list('id', flat=True),
            'started_at': self.started_at,
            'finished_at': self.finished_at,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

        if self.deleted_at:
            response['deleted_at'] = self.deleted_at

        return response
