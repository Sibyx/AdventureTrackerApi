from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from django.db import transaction
from django.db.models import Q
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods

from api import http_status
from api.auth.decorators import token_required
from api.errors import ValidationException, ApiException
from api.forms.sync import SyncForm
from api.response import SingleResponse
from core.models import Adventure, Record, RecordType

User = get_user_model()


def _sync_record(adventure: Adventure, record_data: dict):
    try:
        record = Record.objects_all.get(pk=record_data['id'])
    except Record.DoesNotExist:
        record = Record(id=record_data['id'])

    if record.updated_at is None or record_data['updated_at'] > record.updated_at:
        # Basic data
        record.adventure = adventure
        record.record_type_id = record_data['record_type_id']
        record.user_id = record_data['user_id']
        record.happened_at = record_data['happened_at']
        record.description = record_data['description']
        record.deleted_at = record_data['deleted_at']

        # Location
        if record_data['location'] is not None:
            record.location = Point(
                record_data['location']['latitude'],
                record_data['location']['longitude'],
                record_data['location']['altitude']
            )

        record.save()


def _sync_adventure(user: User, adventure_data: dict):
    try:
        adventure = Adventure.objects_all.get(pk=adventure_data['id'])

        if user not in adventure.users.all():
            raise ApiException(_("You are not member of this adventure!"), status_code=http_status.HTTP_403_FORBIDDEN)
    except Adventure.DoesNotExist:
        adventure = Adventure(id=adventure_data['id'])

    if adventure.updated_at is None or adventure_data['updated_at'] > adventure.updated_at:
        # Basic data
        adventure.status = adventure_data['status']
        adventure.name = adventure_data['name']
        adventure.description = adventure_data['description']
        adventure.started_at = adventure_data['started_at']
        adventure.finished_at = adventure_data['finished_at']
        adventure.deleted_at = adventure_data['deleted_at']

        # Members
        adventure.users.clear()
        if user.id not in adventure_data['members']:
            adventure_data['members'].append(user.id)
        for member in adventure_data['members']:
            adventure.users.add(member)

        adventure.save()

    # Records
    for record in adventure_data['records']:
        _sync_record(adventure, record)


@transaction.atomic
@require_http_methods(['POST'])
@token_required
def sync(request):
    form = SyncForm.create_from_request(request)

    if not form.is_valid():
        raise ValidationException(form)

    # Sync user
    if form.cleaned_data['user']:
        request.user.name = form.cleaned_data['user']['name']
        request.user.surname = form.cleaned_data['user']['surname']
        request.user.save()

    # Sync adventures
    for adventure in form.cleaned_data['adventures']:
        _sync_adventure(request.user, adventure)

    # Create sync response
    adventures = Adventure.objects.filter(users__id=request.user.id)

    if form.cleaned_data['last_sync']:
        last_sync = form.cleaned_data['last_sync']
        adventures = adventures.filter(Q(updated_at__gt=last_sync) | Q(records__updated_at__gt=last_sync)).distinct()

    response = {
        'user': request.user,
        'adventures': [],
        'record_types': RecordType.objects.all(),
    }

    for adventure in adventures:
        conditions = {}

        if form.cleaned_data['last_sync']:
            conditions['updated_at__gt'] = form.cleaned_data['last_sync']

        item = adventure.summary
        item['records'] = adventure.records.filter(**conditions)

        response['adventures'].append(item)

    return SingleResponse(response, status=http_status.HTTP_200_OK)
