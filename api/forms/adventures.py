from django.forms import fields
from django_api_forms import EnumField, FieldList, Form

from core.models.adventure import AdventureStatus


class CreateAdventureForm(Form):
    status = EnumField(enum=AdventureStatus)
    name = fields.CharField(max_length=100)
    description = fields.CharField(required=False)
    started_at = fields.DateTimeField()
    finished_at = fields.DateTimeField(required=False)
    members = FieldList(field=fields.UUIDField(), required=False)
