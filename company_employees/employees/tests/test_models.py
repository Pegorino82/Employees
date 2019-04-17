from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from employees.models import Employee
from units.models import Unit


class TestEmployeeModel(TestCase):

    def setUp(self):
        self.u = Unit.objects.create(title='TestUnit')
        self.e_not_working = Employee.objects.create(
            name='Jack',
            patronymic='D',
            surname='Black',
            birth='1900-01-01',
            email='test@mail.ru',
            phone='79110000000',
            start_work='1950-12-12',
            finish_work='1960-12-12',
            position='position',
            unit=self.u
        )
        self.e_still_working = Employee.objects.create(
            name='Mat',
            patronymic='D',
            surname='Perry',
            birth='1950-01-01',
            email='another@mail.ru',
            phone='79110000000',
            start_work='1950-12-12',
            finish_work=None,
            position='position',
            unit=self.u
        )

    def test_print(self):
        self.assertEqual(str(self.e_not_working), 'Jack D Black')
        self.assertNotEqual(str(self.u), 'Mary')

    def test_error(self):
        with self.assertRaises(ObjectDoesNotExist):
            Employee.objects.get(name='Mary')

    def test_filter_by_unit_and_working(self):
        filtered = Employee.filter_by_unit_and_working()
        self.assertQuerysetEqual(
            filtered,
            Employee.objects.all().order_by('surname'),
            transform=lambda x: x
        )
