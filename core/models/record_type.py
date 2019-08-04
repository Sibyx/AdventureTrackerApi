from django.contrib.gis.db import models

from core.models.base import BaseModel


class RecordType(BaseModel):
    class Meta:
        app_label = 'core'
        default_permissions = ()
        db_table = 'record_types'

    code = models.UUIDField(unique=True)
    description = models.TextField(null=True, blank=True)
