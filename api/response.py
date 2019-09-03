import datetime
import decimal
import json

from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse

from django.contrib.gis.db.models import QuerySet


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


class SingleResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        # TODO: check if content is none in kwargs
        data = {
            'response': data,
            'metadata': []
        }
        kwargs.setdefault('content_type', 'application/json')
        data = json.dumps(data, cls=DjangoJSONEncoder)

        super().__init__(content=data, **kwargs)


class PaginationResponse(HttpResponse):
    def __init__(self, qs: QuerySet, page: int, limit: int, **kwargs):
        # TODO: check if content is none in kwargs
        kwargs.setdefault('content_type', 'application/json')
        paginator = Paginator(qs, limit)

        # Dict serialization using summary
        items = [item.summary for item in paginator.get_page(page)]

        data = {
            'items': items,
            'metadata': {
                'page': int(page),
                'limit': paginator.per_page,
                'pages': paginator.num_pages,
                'total': paginator.count
            }
        }
        data = json.dumps(data, cls=DjangoJSONEncoder)

        super().__init__(content=data, **kwargs)
