from django.contrib import auth
from django.contrib.auth.models import AnonymousUser
from django.urls import resolve
from django.utils.translation import gettext as _
from sentry_sdk import configure_scope

from api import http_status
from api.errors import ApiException


class TokenMiddleware(object):
    def __init__(self, get_response):
        self.WHITELIST = [
            'token-create'
        ]
        self.get_response = get_response

    def __call__(self, request):
        if resolve(request.path_info).url_name in self.WHITELIST:
            return self.get_response(request)

        auth_header = request.headers.get('Authorization', b'').split()

        if not auth_header or auth_header[0].lower() != 'token':
            return ApiException(
                _("Missing token in HTTP request"), status_code=http_status.HTTP_401_UNAUTHORIZED
            ).create_response()

        if len(auth_header) != 2:
            return ApiException(_("Improperly formatted token"), status_code=http_status.HTTP_400_BAD_REQUEST).create_response()

        user = auth.authenticate(token=auth_header[1])

        if user:
            request.user = user
            request.token = user.tokens.get(value=auth_header[1])

            with configure_scope() as scope:
                scope.user = {
                    "id": user.pk,
                    "email": user.email
                }
        else:
            request.user = AnonymousUser()
            request.token = None

        return self.get_response(request)
