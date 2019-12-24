import traceback
from typing import Type

import sentry_sdk
from django.conf import settings
from django_request_formatter.forms import Form

from api import http_status

from django.utils.translation import gettext as _


class ApiException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        previous: Exception = None
    ):
        super().__init__(message)

        self._status_code = status_code
        self._message = message
        self._previous = previous

        with sentry_sdk.push_scope() as scope:
            for key, value in self.__dict__.items():
                scope.set_extra(key, value)

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def message(self) -> str:
        return self._message

    @property
    def previous(self) -> Exception:
        return self._previous

    @property
    def payload(self) -> dict:
        result = {
            'message': self.message,
            'code': self.status_code
        }

        if settings.DEBUG:
            result['trace'] = traceback.format_exc().split("\n")

        return result


class ValidationException(ApiException):
    def __init__(self, form: Form):
        super().__init__(_("Validation error!"), status_code=http_status.HTTP_422_UNPROCESSABLE_ENTITY)
        self._form = form
