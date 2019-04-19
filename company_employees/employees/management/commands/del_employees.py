from django.core.management.base import BaseCommand
import random
from datetime import datetime, date

from employees.models import Employee
from units.models import Unit



class Command(BaseCommand):
    help = '''
    fill test employees to db
    by default creates 300 records
    when flag -a is defined, creates a records: -a 500 creates 500 records
    '''

    def add_arguments(self, parser):
        parser.add_argument('-a')

    def handle(self, *args, **options):

        Employee.objects.all().delete()

