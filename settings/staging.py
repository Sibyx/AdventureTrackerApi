import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from settings.base import *

DEBUG = False

TIME_ZONE = 'UTC'

ALLOWED_HOSTS = [
    'api.adventures.jakubdubec.me'
]

sentry_sdk.init(
    integrations=[DjangoIntegration()]
)
