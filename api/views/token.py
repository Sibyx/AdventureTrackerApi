import uuid

from django.contrib.auth import get_user_model
from django.utils import dateparse
from django.utils.translation import gettext as _
from django.views.generic.base import View

from api import http_status
from api.errors import ApiException
from api.response import SingleResponse
from core.models import Token

User = get_user_model()


class TokenManagement(View):
    def post(self, request):
        password = request.POST.get('password', None)
        username = request.POST.get('username', None)
        expires_at = request.POST.get('expires_at', None)

        conditions = {
            User.USERNAME_FIELD: username
        }

        try:
            user = User.objects.get(**conditions)
        except User.DoesNotExist as e:
            raise ApiException(
                _("Invalid credentials!"), status_code=http_status.HTTP_401_UNAUTHORIZED, previous=e
            )

        if not user.check_password(password):
            raise ApiException(_("Invalid credentials!"),
                               status_code=http_status.HTTP_401_UNAUTHORIZED)

        if not user.is_active or not user.has_perm('add_token'):
            raise ApiException(_("Permission denied!"), status_code=http_status.HTTP_403_FORBIDDEN)

        token = Token.objects.create(
            user=user,
            value=uuid.uuid4(),
            expires_at=dateparse.parse_datetime(expires_at) if expires_at else None
        )

        return SingleResponse(data=token.summary, status=http_status.HTTP_201_CREATED)

