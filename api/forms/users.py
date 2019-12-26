from django.forms import fields
from django_request_formatter.forms import Form


class UpdateUserForm(Form):
    name = fields.CharField(max_length=50)
    surname = fields.CharField(max_length=50)
