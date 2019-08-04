from django.contrib.auth.base_user import BaseUserManager

from core.managers.base import BaseManager


class UserManager(BaseUserManager, BaseManager):
    use_in_migrations = True

    def _create_user(self, **extra_fields):
        if extra_fields.get('email') is not None:
            extra_fields.setdefault('email', self.normalize_email(extra_fields.get('email')))

        user = self.model(**extra_fields)
        user.set_password(extra_fields.get('password'))
        user.save(using=self._db)
        return user

    def create_user(self, **extra_fields):
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(**extra_fields)

    def create_superuser(self, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(**extra_fields)
