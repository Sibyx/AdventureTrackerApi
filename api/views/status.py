from django.utils import timezone
from django.views.decorators.http import require_http_methods

from api import http_status
from api.response import SingleResponse


@require_http_methods(['GET'])
def status(request):
    return SingleResponse({
        'version': '1.0.0',
        'timestamp': timezone.now()
    }, status=http_status.HTTP_200_OK)
