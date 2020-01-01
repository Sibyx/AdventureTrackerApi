from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from django.views.decorators.http import require_http_methods

from api import http_status
from api.auth.decorators import token_required
from api.errors import ValidationException
from api.forms.sync import SyncForm
from api.response import SingleResponse
from api.services.sync import SyncService
from core.models import Adventure, RecordType

User = get_user_model()


@transaction.atomic
@require_http_methods(['POST'])
@token_required
def sync(request):
    form = SyncForm.create_from_request(request)

    if not form.is_valid():
        raise ValidationException(form)

    sync_service = SyncService(request.user, form.cleaned_data['last_sync'])

    # Sync user
    if form.cleaned_data['user']:
        request.user.name = form.cleaned_data['user']['name']
        request.user.surname = form.cleaned_data['user']['surname']
        request.user.save()

    # Sync adventures
    for adventure in form.cleaned_data['adventures']:
        sync_service.sync_adventure(adventure)

    # Create sync response
    adventures = Adventure.objects.filter(users__id=request.user.id)

    if sync_service.last_sync:
        adventures = adventures.filter(
            Q(updated_at__gt=sync_service.last_sync) | Q(records__updated_at__gt=sync_service.last_sync)
        ).distinct()

    response = {
        'user': request.user,
        'adventures': [],
        'record_types': RecordType.objects.all(),
    }

    for adventure in adventures:
        conditions = {}

        if sync_service.last_sync:
            conditions['updated_at__gt'] = sync_service.last_sync

        item = adventure.summary
        item['records'] = adventure.records.filter(**conditions)

        response['adventures'].append(item)

    return SingleResponse(response, status=http_status.HTTP_200_OK)
