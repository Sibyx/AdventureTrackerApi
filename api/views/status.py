import os

import pytz
from django.conf import settings
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from api import http_status
from api.response import SingleResponse


@require_http_methods(['GET'])
def status(request):
    return SingleResponse(request, {
        'version': '1.0.0',
        'deployed_at': timezone.datetime.fromtimestamp(
            os.path.getmtime(settings.BASE_DIR), pytz.timezone(settings.TIME_ZONE)
        ),
        'timestamp': timezone.now()
    }, status=http_status.HTTP_200_OK)
