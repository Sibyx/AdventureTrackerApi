from django.contrib import auth
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext as _

from api import http_status
from api.errors import ApiException
from api.response import ErrorResponse


class TokenMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get('Authorization', b'').split()

        if not auth_header:
            return self.get_response(request)

        if len(auth_header) != 2:
            return ErrorResponse.create_from_exception(
                ApiException(request, _("Improperly formatted token"), status_code=http_status.HTTP_400_BAD_REQUEST)
            )

        user = auth.authenticate(token=auth_header[1])

        if user:
            request.user = user
            request.token = user.tokens.get(pk=auth_header[1])
        else:
            request.user = AnonymousUser()
            request.token = None

        return self.get_response(request)
