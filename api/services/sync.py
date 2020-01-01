from datetime import datetime
from typing import List, Union
from uuid import UUID

from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from django.utils.translation import gettext as _

from api import http_status
from api.errors import ApiException
from core.models import Record, Photo, Adventure

User = get_user_model()


class SyncService(object):
    def __init__(self, user: User, last_sync: datetime = None):
        self._user = user
        self._last_sync = last_sync

    @property
    def last_sync(self) -> Union[datetime, None]:
        return self._last_sync

    def sync_adventure(self, adventure_data: dict):
        try:
            adventure = Adventure.objects_all.get(pk=adventure_data['id'])

            if self._user not in adventure.users.all():
                raise ApiException(_("You are not member of this adventure!"),
                                   status_code=http_status.HTTP_403_FORBIDDEN)
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
            if self._user.id not in adventure_data['members']:
                adventure_data['members'].append(self._user.id)
            for member in adventure_data['members']:
                adventure.users.add(member)

            adventure.save()

        # Records
        for record in adventure_data['records']:
            self._sync_record(adventure, record)

    def _sync_photos(self, record: Record, photos: List[UUID]):
        if self._last_sync:
            existing_photos = record.photos.filter(created_at__gt=self._last_sync).values_list('id', flat=True)
        else:
            existing_photos = record.photos.values_list('id', flat=True)

        for photo_id in photos:
            if not record.photos.filter(pk=photo_id).exists():
                Photo.objects.create(
                    id=photo_id,
                    record=record,
                )
        exclude_photos = photos + list(existing_photos)
        record.photos.exclude(id__in=exclude_photos).delete()

    def _sync_record(self, adventure: Adventure, record_data: dict):
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

        # Sync photos
        if record_data['photos']:
            self._sync_photos(record, record_data['photos'])
