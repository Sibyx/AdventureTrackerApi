from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import get_language

from core.models.base import BaseModel


class RecordType(BaseModel):
    class Meta:
        app_label = 'core'
        default_permissions = ()
        db_table = 'record_types'

    code = models.CharField(max_length=50, unique=True)
    localizations = JSONField()

    @property
    def summary(self) -> dict:
        # Check if language code exists in model localizations
        language_code = get_language() if get_language() in self.localizations else settings.LANGUAGE_CODE

        return {
            'code': self.code,
            'title': self.localizations[language_code]['title'],
            'description': self.localizations[language_code]['description'],
            'examples': self.localizations[language_code]['examples'],
            'create_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
