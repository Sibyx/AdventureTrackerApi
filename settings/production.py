import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from settings.base import *

DEBUG = False

TIME_ZONE = 'UTC'

ALLOWED_HOSTS = [
    'adventures.jakubdubec.me'
]

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[DjangoIntegration()]
)
