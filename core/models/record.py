from django.contrib.gis.db import models

from core.models.adventure import Adventure
from core.models.record_type import RecordType
from core.models.base import BaseModel
from core.models.user import User


class Record(BaseModel):
    class Meta:
        app_label = 'core'
        default_permissions = ()
        db_table = 'records'

    adventure = models.ForeignKey(Adventure, on_delete=models.CASCADE, related_name='records')
    record_type = models.ForeignKey(RecordType, on_delete=models.CASCADE, related_name='records')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='records')
    code = models.UUIDField(unique=True)
    happened_at = models.DateTimeField()
    description = models.TextField()
    location = models.PointField(null=True, blank=True)
