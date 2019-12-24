import datetime
import decimal
from enum import Enum
from uuid import UUID

from django.core.paginator import Page
from django.core.serializers.json import DjangoJSONEncoder

from core.models.base import BaseModel


class ApiJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, BaseModel):
            return o.summary
        if isinstance(o, UUID):
            return str(o)
        if isinstance(o, Page):
            return o.object_list
        if isinstance(o, Enum):
            return o.value
        return DjangoJSONEncoder.default(self, o)


class MessagePackEncoder(object):
    """
    TODO: MessagePack according  accept-type
    https://github.com/juanriaza/django-rest-framework-msgpack/blob/master/rest_framework_msgpack/renderers.py
    """

    def encode(self, obj):
        if isinstance(obj, datetime.datetime):
            return {'__class__': 'datetime', 'as_str': obj.isoformat()}
        elif isinstance(obj, datetime.date):
            return {'__class__': 'date', 'as_str': obj.isoformat()}
        elif isinstance(obj, datetime.time):
            return {'__class__': 'time', 'as_str': obj.isoformat()}
        elif isinstance(obj, decimal.Decimal):
            return {'__class__': 'decimal', 'as_str': str(obj)}
        else:
            return obj
