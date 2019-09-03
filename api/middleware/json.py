import json
from django.utils.translation import gettext as _

from django.http import QueryDict

from api import http_status
from api.errors import ApiException


class JsonMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.META.get('CONTENT_TYPE') and 'application/json' in request.META.get('CONTENT_TYPE'):
            try:
                data = json.loads(request.body)
                query_data = QueryDict('', mutable=True)
                for key, value in data.items():
                    if isinstance(value, list):
                        for x in value:
                            query_data.update({key: x})
                    else:
                        query_data.update({key: value})

                if request.method == 'POST':
                    request.POST = query_data

                return self.get_response(request)
            except json.JSONDecodeError:
                return ApiException(
                    _("JSON Decode Error"), status_code=http_status.HTTP_400_BAD_REQUEST
                ).create_response()
        return self.get_response(request)
