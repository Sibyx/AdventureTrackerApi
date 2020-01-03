from functools import wraps
from gettext import gettext as _

from api import http_status
from api.errors import ApiException


def token_required(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if not hasattr(request, 'user') or not request.user or not request.user.is_authenticated:
            raise ApiException(_("Invalid or missing credentials"), status_code=http_status.HTTP_401_UNAUTHORIZED)
        return func(request, *args, **kwargs)

    return inner
