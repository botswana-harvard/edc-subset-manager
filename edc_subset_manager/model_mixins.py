from django.apps import apps as django_apps
from django.db import models


def get_device_id():
    return django_apps.get_app_config('edc_device').device_id


class SubsetModelMixin(models.Model):

    device_id = models.CharField(
        max_length=5,
        default=get_device_id)

    class Meta:
        abstract = True
