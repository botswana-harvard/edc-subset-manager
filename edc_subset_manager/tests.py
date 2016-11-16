from django.apps import apps as django_apps
from django.test.testcases import TestCase
from edc_device.constants import CLIENT, CENTRAL_SERVER

from example.models import ReferenceModel, CrfModel


class Tests(TestCase):

    def setUp(self):
        self.edc_device_app_config = django_apps.get_app_config('edc_device')
        self.app_config = django_apps.get_app_config('edc_subset_manager')
        self.edc_device_app_config.device_id = '00'
        self.app_config.role = CLIENT
        for device_id in ['00', '10', '20', '30', '40']:
            for i in range(int(device_id), int(device_id) + 10):
                reference_model = ReferenceModel.objects.create(
                    device_id=device_id,
                    reference_value='value' + device_id,
                    subset_value=str(i))
                CrfModel.objects.create(reference_model=reference_model)

    def test_active_as_client(self):
        self.edc_device_app_config.device_id = '00'
        self.app_config.role = CLIENT
        app_config = django_apps.get_app_config('edc_subset_manager')
        self.assertEqual(app_config.role, CLIENT)
        self.assertTrue(app_config.active)

    def test_active_as_server(self):
        self.edc_device_app_config.device_id = '99'
        self.app_config.role = CENTRAL_SERVER
        self.assertTrue(self.edc_device_app_config.role == CENTRAL_SERVER)
        self.assertTrue(django_apps.get_app_config('edc_subset_manager').role == CENTRAL_SERVER)
        self.assertTrue(django_apps.get_app_config('edc_device').device_id == '99')
        self.assertTrue(django_apps.get_app_config('edc_device').role == CENTRAL_SERVER)
        self.assertTrue(self.app_config.active)
        self.assertEqual(CrfModel.objects.all().count(), 50)

    def test_subset_filtering(self):
        self.edc_device_app_config.device_id = '00'
        self.app_config.role = CLIENT
        self.assertEqual(ReferenceModel.objects.filter(device_id='00').count(), 10)
        self.assertEqual(ReferenceModel.objects.filter(reference_value='value00', device_id='00').count(), 10)
        self.assertEqual(CrfModel.objects.all().count(), 10)

    def test_subset_filtering2(self):
        self.edc_device_app_config.device_id = '10'
        self.app_config.role = CLIENT
        self.assertEqual(CrfModel.objects.all().count(), 10)

    def test_update(self):
        self.edc_device_app_config.device_id = '00'
        self.app_config.role = CLIENT
        for obj in CrfModel.objects.all()[0:5]:
            obj.field1 = 'erik'
            obj.save()
        self.assertEqual(CrfModel.objects.filter(field1='erik').count(), 5)

    def test_bulk_update(self):
        self.edc_device_app_config.device_id = '00'
        self.app_config.role = CLIENT
        CrfModel.objects.update(field1='erik')
        self.assertEqual(CrfModel.objects.filter(field1='erik').count(), 10)

    def test_bulk_update2(self):
        self.edc_device_app_config.device_id = '00'
        self.app_config.role = CLIENT
        CrfModel.objects.update(field1='erik')
        self.assertEqual(CrfModel.objects.filter(field1='erik').count(), 10)
        self.edc_device_app_config.device_id = '99'
        self.app_config.role = CENTRAL_SERVER
        self.assertEqual(CrfModel.objects.filter(field1='erik').count(), 10)

    def test_bulk_update3(self):
        self.edc_device_app_config.device_id = '99'
        self.app_config.role = CENTRAL_SERVER
        CrfModel.objects.update(field1='erik')
        self.assertEqual(CrfModel.objects.filter(field1='erik').count(), 50)
        self.edc_device_app_config.device_id = '00'
        self.app_config.role = CLIENT
        self.assertEqual(CrfModel.objects.filter(field1='erik').count(), 10)
