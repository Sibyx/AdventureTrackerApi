from django.forms import fields
from django_request_formatter.fields import FormField
from django_request_formatter.forms import Form


class PointForm(Form):
    latitude = fields.FloatField()
    longitude = fields.FloatField()
    altitude = fields.FloatField(required=False)


class CreateRecordForm(Form):
    record_type_id = fields.UUIDField()
    user_id = fields.UUIDField()
    happened_at = fields.DateTimeField()
    description = fields.CharField(required=False)
    point = FormField(form=PointForm, required=False)
