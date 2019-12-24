from django.forms import fields
from django_request_formatter.forms import Form


class CreateTokenForm(Form):
    username = fields.EmailField(required=True)
    password = fields.CharField(max_length=50)
    expires_at = fields.DateTimeField(required=False)
