from django.urls import path

from api.views import token

urlpatterns = [
    path('tokens', token.create_token, name='token-create'),
    path('tokens/validate', token.validate_token, name='token-validate'),
]
