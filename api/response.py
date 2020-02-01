import json
from dataclasses import dataclass
from enum import Enum

import msgpack
from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.utils.translation import gettext as _

from api import http_status
from api.encoders import ApiJSONEncoder, MessagePackEncoder
from api.errors import ValidationException, ApiException


@dataclass
class Ordering:
    class Order(Enum):
        ASC = 'asc'
        DESC = 'desc'

    column: str
    order: Order = Order.ASC

    @classmethod
    def create_from_request(cls, request, aliases: dict = None) -> 'Ordering':
        column = request.GET.get('order_by', 'created_at')
        aliases = aliases or {}

        for key, value in aliases.items():
            if column == key:
                column = value
                break

        result = Ordering(column, Ordering.Order(request.GET.get('order', 'asc')))
        return result

    def __str__(self):
        return self.column if self.order == self.Order.ASC else f"-{self.column}"

    def __repr__(self):
        return self.__str__()


class GeneralResponse(HttpResponse):
    def __init__(self, request, data: dict = None, **kwargs):
        params = {}
        if data is not None:
            content_type = request.headers.get('accept', 'application/json')
            if content_type == 'application/x-msgpack':
                params['content_type'] = 'application/x-msgpack'
                params['content'] = msgpack.packb(data, use_bin_type=True, default=MessagePackEncoder().encode)
            elif content_type in ['*/*', 'application/json']:
                params['content_type'] = 'application/json'
                params['content'] = json.dumps(data, cls=ApiJSONEncoder)
            else:
                params['content_type'] = 'application/json'
                params['status'] = http_status.HTTP_406_NOT_ACCEPTABLE
                params['content'] = json.dumps({
                    'message': _("Not Acceptable"),
                    'metadata': {
                        'available': [
                            'application/json',
                            'application/x-msgpack'
                        ],
                        'asked': content_type
                    }
                })

        kwargs.update(params)
        super().__init__(**kwargs)


class SingleResponse(GeneralResponse):
    def __init__(self, request, data=None, **kwargs):
        if data is None:
            kwargs['status'] = http_status.HTTP_204_NO_CONTENT
        else:
            data = {
                'response': data,
            }
        super().__init__(request=request, data=data, **kwargs)


class ErrorResponse(GeneralResponse):
    def __init__(self, request, payload: dict, **kwargs):
        data = {
            'error': payload,
            'metadata': {}
        }

        super().__init__(request=request, data=data, **kwargs)

    @staticmethod
    def create_from_exception(e: ApiException) -> 'ErrorResponse':
        return ErrorResponse(e.request, e.payload, status=e.status_code)


class ValidationResponse(GeneralResponse):
    def __init__(self, request, payload: dict, **kwargs):
        data = {
            'errors': payload
        }

        super().__init__(request, data, status=http_status.HTTP_422_UNPROCESSABLE_ENTITY, **kwargs)

    @staticmethod
    def create_from_exception(e: ValidationException) -> 'ValidationResponse':
        return ValidationResponse(e.request, e.payload, status=http_status.HTTP_422_UNPROCESSABLE_ENTITY)


class PaginationResponse(GeneralResponse):
    def __init__(
        self, request, qs, page: int, limit: int = settings.PAGINATION['PER_PAGE'], ordering: Ordering = None, **kwargs
    ):
        kwargs.setdefault('content_type', 'application/json')

        # Ordering
        ordering = ordering if ordering else Ordering('created_at')
        qs = qs.order_by(str(ordering))
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
        super().__init__(request, data, **kwargs)


__all__ = [
    "SingleResponse",
    "ErrorResponse",
    "PaginationResponse",
    "ValidationResponse"
]
