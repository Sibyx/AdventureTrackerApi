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
    happened_at = models.DateTimeField()
    description = models.TextField()
    location = models.PointField(null=True, blank=True, dim=3)

    def summary(self) -> dict:
        response = {
            'id': self.id,
            'adventure_id': self.adventure_id,
            'record_type_id': self.record_type_id,
            'user_id': self.user_id,
            'happened_at': self.happened_at,
            'description': self.description
        }

        if self.location:
            response['location'] = {
                'latitude': self.location.x,
                'longitude': self.location.y,
                'altitude': self.location.z
            }

        if self.deleted_at:
            response['deleted_at'] = self.deleted_at

        return response
