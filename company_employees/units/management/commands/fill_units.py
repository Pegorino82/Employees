from django.core.management.base import BaseCommand

from units.models import Unit

UNITS = (Unit(title=f'unit_{i}') for i in range(1, 11))


class Command(BaseCommand):
    help = '''
    fill test units to db
    by default creates 10 records
    when flag -a is defined, creates a records: -a 15 creates 15 records
    '''

    def add_arguments(self, parser):
        parser.add_argument('-a')

    def handle(self, *args, **options):
        n = 10
        if options.get('a'):
            n = int(options.get('a'))
        Unit.objects.bulk_create((Unit(title=f'unit_{i}') for i in range(1, n + 1)))
