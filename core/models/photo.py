from django.contrib.gis.db import models

from core.models.record import Record
from core.models.base import BaseModel


class Photo(BaseModel):
    class Meta:
        app_label = 'core'
        default_permissions = ()
        db_table = 'photos'

    def _upload_to_path(self, filename):
        return f"photos/{self.record.id}/{filename}"

    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name='record')
    code = models.UUIDField(unique=True)
    mime = models.CharField(max_length=50, null=True, blank=True)
    happened_at = models.DateTimeField(null=True, blank=True)
    path = models.ImageField(upload_to=_upload_to_path)
