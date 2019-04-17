from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command
from employees.models import Employee
from units.models import Unit


class TestEmployeeViews(TestCase):

    def setUp(self):
        call_command('flush', '--noinput')
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
        self.client = Client()

    def test_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/employees')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/employees/surname')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/employees/surname?start=А&stop=Б')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/employees/1')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/employees/10')
        self.assertEqual(response.status_code, 404)


