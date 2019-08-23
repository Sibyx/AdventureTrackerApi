from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from api import http_status
from api.auth.decorators import token_required
from api.response import SingleResponse


@require_http_methods(['GET'])
@token_required
def validate(request):
    return SingleResponse(data=request.token.summary, status=http_status.HTTP_200_OK)


@require_http_methods(['DELETE'])
@token_required
def logout(request):
    request.token.hard_delete()
    return HttpResponse(content=None, status=http_status.HTTP_204_NO_CONTENT)
