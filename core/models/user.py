from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.gis.db import models

from core.models.adventure import Adventure
from core.models.base import BaseModel


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    class Meta:
        app_label = 'core'
        default_permissions = ()
        db_table = 'users'

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    surname = models.CharField(max_length=50, null=True, blank=True)
    adventures = models.ManyToManyField(Adventure, related_name='users')

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    def get_full_name(self) -> str:
        return f'{self.name} {self.surname}'

    def get_short_name(self) -> str:
        return self.name

    @property
    def is_staff(self):
        return self.is_superuser

    def __str__(self):
        return self.email
