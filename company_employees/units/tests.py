from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from units.models import Unit


class TestUnitModel(TestCase):

    def setUp(self):
        self.u = Unit.objects.create(title='TestUnit')

    def test_print(self):

        self.assertEqual(str(self.u), 'TestUnit')
        self.assertNotEqual(str(self.u), '321')

    def test_error(self):
        with self.assertRaises(ObjectDoesNotExist):
            Unit.objects.get(title='123')


