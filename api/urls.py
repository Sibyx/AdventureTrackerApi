from django.urls import path

from api.views import token, auth, record_type, sync, status

urlpatterns = [
    # Tokens
    path('tokens', token.TokenManagement.as_view()),

    # Record types
    path('record_types', record_type.RecordTypeManagement.as_view()),

    # Sync
    path('sync', sync.sync, name='sync'),

    # Auth
    path('auth/validate', auth.validate, name='auth-create'),
    path('auth/logout', auth.logout, name='auth-logout'),

    # Status
    path('status', status.status, name='status'),
]
