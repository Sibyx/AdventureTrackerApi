from django.forms import fields
from django_api_forms import FormField, FieldList, Form


class PointForm(Form):
    latitude = fields.FloatField()
    longitude = fields.FloatField()
    altitude = fields.FloatField(required=False)


class CreateRecordForm(Form):
    record_type_id = fields.UUIDField()
    user_id = fields.UUIDField()
    happened_at = fields.DateTimeField()
    description = fields.CharField(required=False)
    location = FormField(form=PointForm, required=False)
    photos = FieldList(field=fields.UUIDField(), required=False)
