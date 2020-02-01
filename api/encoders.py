import datetime
import decimal
from enum import Enum
from uuid import UUID

from django.core.paginator import Page
from django.core.serializers.json import DjangoJSONEncoder

from core.models.base import BaseModel
from core.querysets.base import BaseQuerySet


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
        if isinstance(o, BaseQuerySet):
            return list(o)
        return DjangoJSONEncoder.default(self, o)


class MessagePackEncoder(object):
    def encode(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.time):
            return obj.isoformat()
        elif isinstance(obj, decimal.Decimal):
            return str(obj)
        elif isinstance(obj, UUID):
            return str(obj)
        elif isinstance(obj, BaseModel):
            return obj.summary
        elif isinstance(obj, Page):
            return obj.object_list
        elif isinstance(obj, Enum):
            return str(obj.value)
        elif isinstance(obj, BaseQuerySet):
            return list(obj)
        else:
            return obj
