import uuid

from django.contrib.gis.db import models
from django.utils import timezone

from core.managers.base import BaseManager


class BaseModel(models.Model):
    class Meta:
        abstract = True
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = BaseManager()
    objects_all = BaseManager(alive_only=False)

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super(BaseModel, self).delete()

    @property
    def summary(self) -> dict:
        """
        Exception, ktorej uloha je upozornit na to, ze by default modely nie su serializovatelne a kazdy model
        ma tuto metodu pretazit, ak bude vystupom z API
        :return:
        """
        raise RuntimeError("Not implemented summary property!")
