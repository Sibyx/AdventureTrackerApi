import io
import os
from datetime import datetime

from PIL import Image
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic.base import View
from django.utils.timezone import make_aware

from api import http_status
from api.auth.decorators import token_required
from api.errors import ApiException
from api.response import SingleResponse
from core.models import Photo


class PhotoDetailView(View):
    @method_decorator(transaction.atomic)
    @method_decorator(token_required)
    def post(self, request, photo_id):
        try:
            photo = Photo.objects.get(pk=photo_id)
        except Photo.DoesNotExist:
            raise ApiException(_("Photo not found!"), status_code=http_status.HTTP_404_NOT_FOUND)

        if request.user not in photo.record.adventure.users.all():
            raise ApiException(_("Access forbidden!"), status_code=http_status.HTTP_403_FORBIDDEN)

        stream = io.BytesIO(request.body)
        pillow_image = Image.open(stream)
        exif = pillow_image.getexif()

        photo.mime = Image.MIME[pillow_image.format]

        if photo.mime not in settings.ALLOWED_PHOTO_MIMES or request.headers.get('Content-Type') != photo.mime:
            raise ApiException(_('Invalid content type detected!'), status_code=http_status.HTTP_400_BAD_REQUEST)

        filename = f"{photo.id}.{pillow_image.format.lower()}"
        uploaded_file = InMemoryUploadedFile(
            stream, None, filename, Image.MIME[pillow_image.format], pillow_image.size, None
        )

        # EXIF36867 - DateTimeOriginal
        # FIXME: timezones
        if exif.get(36867):
            photo.happened_at = make_aware(datetime.strptime(exif.get(36867), "%Y:%m:%d %H:%M:%S"))
        else:
            photo.happened_at = None

        photo.path.delete()
        photo.path.save(filename, uploaded_file)

        photo.save()

        return SingleResponse(photo)

    @method_decorator(token_required)
    def get(self, request, photo_id):
        try:
            photo = Photo.objects.get(pk=photo_id)
        except Photo.DoesNotExist:
            raise ApiException(_("Photo not found!"), status_code=http_status.HTTP_404_NOT_FOUND)

        if request.user not in photo.record.adventure.users.all():
            raise ApiException(_("Access forbidden!"), status_code=http_status.HTTP_403_FORBIDDEN)

        response = HttpResponse(content_type=photo.mime)
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(photo.path.file.name)}'
        response.write(photo.path.read())

        return response
