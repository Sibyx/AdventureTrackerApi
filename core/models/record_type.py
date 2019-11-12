from typing import List

from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import get_language
from pydantic.dataclasses import dataclass

from api.errors import ApiException
from core.models.base import BaseModel

from django.utils.translation import gettext as _


@dataclass
class RecordTypeLocalization(object):
    title: str
    description: str
    examples: List[str]

    @staticmethod
    def create_from_dict(data: dict) -> 'RecordTypeLocalization':
        return RecordTypeLocalization(
            title=data['title'],
            description=data['description'],
            examples=data['examples']
        )

    @property
    def summary(self) -> dict:
        return {
            'title': self.title,
            'description': self.description,
            'examples': self.examples
        }


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

        try:
            localization = RecordTypeLocalization.create_from_dict(self.localizations[language_code])
        except KeyError as e:
            raise ApiException(_("Invalid RecordType localization values"), previous=e)

        return {
            'code': self.code,
            'title': localization.title,
            'description': localization.description,
            'examples': localization.examples,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
