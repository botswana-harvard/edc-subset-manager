from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured

from edc_device.constants import CENTRAL_SERVER, NODE_SERVER


class SubsetManagerException(Exception):
    pass


class SubsetManagerMixin:

    reference_model = None  # e.g. plot
    reference_attr = None  # on reference model, e.g. plot.community
    subset_attr = None  # on reference model, e.g. plot.plot_identifier
    to_reference_model = []  # list of model relations to get to reference_model, includes reference_model
    lookup_sep = '__'
    servers = [NODE_SERVER]
    central_server = CENTRAL_SERVER

    def get_queryset(self):
        app_config = django_apps.get_app_config('edc_subset_manager')
        reference_list = self.reference_list
        if app_config.active and reference_list:
            options = {self.lookup_sep.join(self.to_reference_model + [self.subset_attr, 'in']): reference_list}
            return super(SubsetManagerMixin, self).get_queryset().filter(**options)
        return super(SubsetManagerMixin, self).get_queryset()

    @property
    def reference_value(self):
        """override, e.g. community"""
        raise ImproperlyConfigured('Override this method. See manager {}.{}'.format(
            self.model._meta.label_lower, self.__class__.__name__))

    @property
    def reference_list(self):
        app_config = django_apps.get_app_config('edc_subset_manager')
        reference_list = []
        if app_config.role != self.central_server:
            reference_model = django_apps.get_model(*self.reference_model.split('.'))
            options = {self.reference_attr: self.reference_value}
            if app_config.role not in self.servers:
                options.update({'device_id': self.device_id})
            for obj in reference_model.objects.filter(**options):
                reference_list.append(getattr(obj, self.subset_attr))
        return reference_list

    @property
    def device_id(self):
        return django_apps.get_app_config('edc_device').device_id
