from django.urls import path

from api.views import token, auth

urlpatterns = [
    # Tokens
    path('tokens', token.TokenManagement.as_view()),

    # Auth
    path('auth/validate', auth.validate, name='auth-create'),
    path('auth/logout', auth.logout, name='auth-logout'),
]
