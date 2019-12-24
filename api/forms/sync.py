from django.forms import fields
from django_request_formatter.fields import FormFieldList
from django_request_formatter.forms import Form

from api.forms.adventures import CreateAdventureForm
from api.forms.records import CreateRecordForm


class SyncRecordForm(CreateRecordForm):
    id = fields.UUIDField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()
    deleted_at = fields.DateTimeField(required=False)


class SyncAdventureForm(CreateAdventureForm):
    id = fields.UUIDField()
    records = FormFieldList(form=SyncRecordForm)
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()
    deleted_at = fields.DateTimeField(required=False)


class SynchronizationForm(Form):
    last_sync = fields.DateTimeField(required=False)
    adventures = FormFieldList(form=SyncAdventureForm, required=False)
