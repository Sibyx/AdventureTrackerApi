from django.forms import fields
from django_request_formatter.fields import FormFieldList, FormField
from django_request_formatter.forms import Form

from api.forms.adventures import CreateAdventureForm
from api.forms.records import CreateRecordForm
from api.forms.users import UpdateUserForm


class SyncRecordForm(CreateRecordForm):
    id = fields.UUIDField()
    updated_at = fields.DateTimeField()
    deleted_at = fields.DateTimeField(required=False)


class SyncAdventureForm(CreateAdventureForm):
    id = fields.UUIDField()
    records = FormFieldList(form=SyncRecordForm)
    updated_at = fields.DateTimeField()
    deleted_at = fields.DateTimeField(required=False)


class SyncForm(Form):
    last_sync = fields.DateTimeField(required=False)
    user = FormField(form=UpdateUserForm, required=False)
    adventures = FormFieldList(form=SyncAdventureForm, required=False)
