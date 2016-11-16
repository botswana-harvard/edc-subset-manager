from django.apps import AppConfig as DjangoAppConfig
from django.apps import apps as django_apps

from edc_device.constants import CLIENT


class AppConfig(DjangoAppConfig):
    name = 'edc_subset_manager'
    role = CLIENT

    @property
    def active(self):
        if self.role:
            return django_apps.get_app_config('edc_device').role == self.role
        return False
