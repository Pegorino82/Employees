from django.core.management.base import BaseCommand
import random
from datetime import datetime, date

from employees.models import Employee
from units.models import Unit


def date_transform(date_str, format_="%Y-%m-%d"):
    '''Преобразует строку формата 2001-01-01 в объект datetime'''
    return datetime.strptime(date_str, format_).date()


def random_date(a, b):
    '''возвращает случайную дату в интервале [a - b]'''
    year = random.randint(a, b)
    month = random.randint(1, 12)
    day = random.randint(1, 31)
    try:
        date_ = date_transform(f'{year}-{month}-{day}')
        return date_
    except:
        return random_date(a, b)


def finish_work_date(start_work):
    '''возвращает дату окончания работы меньше чем текущая дата и больше чем start_work дата'''
    tmp_date = random_date(start_work.year, random.randint(start_work.year, datetime.today().year))
    if date.today() > tmp_date > start_work:
        return tmp_date
    else:
        return None


with open('surnames.txt', 'r', encoding='utf-8') as f:
    surnames = f.readlines()

with open('names.txt', 'r', encoding='utf-8') as f:
    names = f.readlines()

UNITS = Unit.objects.all()
NAMES = [i.strip().split(' ')[1] for i in names]
PATRONYMICS = [f'{i}ович' for i in NAMES]
SURNAMES = [i.strip().split(' ')[1] for i in surnames]
DOMAINS = ['company.ru', 'personal.ru']
PHONES = ['7911', '7912', '7913']
POSITIONS = [f'Position_{i}' for i in range(1, 11)]


def employees():
    name = random.choice(NAMES)
    patronymic = random.choice(PATRONYMICS)
    surname = random.choice(SURNAMES)
    birth = random_date(1950, 1995)
    email = f'{name[0].lower()}.{surname.lower()}@{random.choice(DOMAINS)}'
    phone = f'+{random.choice(PHONES)}{random.randint(1000000, 9999999)}'
    start_work = random_date(birth.year + 18, 2018)
    finish_work = finish_work_date(start_work)
    position = random.choice(POSITIONS)
    unit = random.choice(UNITS)

    return {
        'name': name,
        'patronymic': patronymic,
        'surname': surname,
        'birth': birth,
        'email': email,
        'phone': phone,
        'start_work': start_work,
        'finish_work': finish_work,
        'position': position,
        'unit': unit
    }


class Command(BaseCommand):
    help = '''
    fill test employees to db
    by default creates 300 records
    when flag -a is defined, creates a records: -a 500 creates 500 records
    '''

    def add_arguments(self, parser):
        parser.add_argument('-a')

    def handle(self, *args, **options):
        n = 300
        if options.get('a'):
            n = int(options.get('a'))
        Employee.objects.all().delete()
        emps = (Employee(**employees()) for _ in range(n))
        Employee.objects.bulk_create(emps)
