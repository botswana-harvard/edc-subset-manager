from django.apps import apps as django_apps
from django.db import models

from edc_subset_manager.manager_mixins import SubsetManagerMixin
from edc_subset_manager.model_mixins import SubsetModelMixin


def my_reference_value():
    return 'value00'


class Manager(SubsetManagerMixin, models.Manager):
    reference_model = 'example.referencemodel'
    reference_attr = 'reference_value'
    to_reference_model = ['reference_model']
    subset_attr = 'subset_value'

    @property
    def reference_value(self):
        return 'value' + django_apps.get_app_config('edc_device').device_id


class ReferenceModel(SubsetModelMixin, models.Model):

    reference_value = models.CharField(
        max_length=10)

    subset_value = models.CharField(
        max_length=10)

    class Meta:
        app_label = 'example'


class CrfModel(models.Model):

    field1 = models.CharField(
        max_length=15,
        null=True)

    reference_model = models.ForeignKey(ReferenceModel)

    objects = Manager()

    class Meta:
        app_label = 'example'
