from django.conf import settings
from django.utils.translation import get_language
from django.views.generic.base import View

from api.response import PaginationResponse, Ordering
from core.models import RecordType


class RecordTypeManagement(View):
    def post(self, request):
        pass

    def get(self, request):
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', settings.PAGINATION['LIMIT'])
        language_code = get_language() or settings.LANGUAGE_CODE

        parameters = {
            'code__icontains': request.GET.get('code', None),
            f'localizations__{language_code}__title__icontains': request.GET.get('title', None),
            f'localizations__{language_code}__description__icontains': request.GET.get('description', None),
        }

        # Remove None values from parameters
        parameters = {k: v for k, v in parameters.items() if v is not None}

        aliases = {
            'title': f'localizations__{language_code}__title'
        }
        ordering = Ordering.create_from_request(request, aliases)

        qs = RecordType.objects.filter(**parameters)

        return PaginationResponse(qs, page, limit, ordering=ordering)


