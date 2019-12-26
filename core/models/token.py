from django.contrib.gis.db import models

from core.models.user import User
from core.models.base import BaseModel


class Token(BaseModel):
    class Meta:
        app_label = 'core'
        default_permissions = ('add', 'delete')
        db_table = 'tokens'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')
    expires_at = models.DateTimeField(null=True, blank=True)

    @property
    def summary(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'expires_at': self.expires_at if self.expires_at else None,
            'created_at': self.created_at
        }
