import json
from dataclasses import dataclass
from enum import Enum

from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse

from api import http_status
from api.encoders import ApiJSONEncoder
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


class SingleResponse(HttpResponse):
    def __init__(self, data: dict, **kwargs):
        data = {
            'response': data,
        }
        kwargs.setdefault('content_type', 'application/json')
        data = json.dumps(data, cls=ApiJSONEncoder)

        super().__init__(content=data, **kwargs)


class ErrorResponse(HttpResponse):
    def __init__(self, payload: dict, **kwargs):
        data = {
            'error': payload,
            'metadata': {}
        }

        kwargs.setdefault('content_type', 'application/json')
        data = json.dumps(data, cls=ApiJSONEncoder)

        super().__init__(content=data, **kwargs)

    @staticmethod
    def create_from_exception(e: ApiException) -> 'ErrorResponse':
        return ErrorResponse(e.payload, status=e.status_code)


class ValidationResponse(HttpResponse):
    def __init__(self, payload: dict, **kwargs):
        data = {
            'errors': payload
        }

        kwargs.setdefault('content_type', 'application/json')
        data = json.dumps(data, cls=ApiJSONEncoder)

        super().__init__(content=data, **kwargs)

    @staticmethod
    def create_from_exception(e: ValidationException) -> 'ValidationResponse':
        return ValidationResponse(e.payload, status=http_status.HTTP_422_UNPROCESSABLE_ENTITY)


class PaginationResponse(HttpResponse):
    def __init__(
        self, qs, page: int, limit: int = settings.PAGINATION['PER_PAGE'], ordering: Ordering = None, **kwargs
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

        data = json.dumps(data, cls=ApiJSONEncoder)

        super().__init__(content=data, **kwargs)
