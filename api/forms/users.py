from django.forms import fields
from django_api_forms import Form


class UpdateUserForm(Form):
    name = fields.CharField(max_length=50)
    surname = fields.CharField(max_length=50)
