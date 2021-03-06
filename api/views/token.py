from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.views.generic.base import View

from api import http_status
from api.errors import ApiException, ValidationException
from api.forms.tokens import CreateTokenForm
from api.response import SingleResponse
from core.models import Token

User = get_user_model()


class TokenManagement(View):
    def post(self, request):
        form = CreateTokenForm.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(form)

        conditions = {
            User.USERNAME_FIELD: form.cleaned_data['username']
        }

        try:
            user = User.objects.get(**conditions)
        except User.DoesNotExist as e:
            raise ApiException(
                request, _("Invalid credentials!"), status_code=http_status.HTTP_401_UNAUTHORIZED, previous=e
            )

        if not user.check_password(form.cleaned_data['password']):
            raise ApiException(request, _("Invalid credentials!"), status_code=http_status.HTTP_401_UNAUTHORIZED)

        if not user.is_active or not user.has_perm('add_token'):
            raise ApiException(request, _("Permission denied!"), status_code=http_status.HTTP_403_FORBIDDEN)

        token = Token.objects.create(
            user=user,
            expires_at=form.cleaned_data['expires_at']
        )

        return SingleResponse(request, data=token.summary, status=http_status.HTTP_201_CREATED)
