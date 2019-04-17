from django.db import models
from django.db.models import Q
from functools import reduce
from collections import OrderedDict

from units.models import Unit

ALPHAS = []
for i in range(1040, 1072):
    if i not in (1066, 1067, 1068):
        ALPHAS.append(chr(i))


class Employee(models.Model):
    name = models.CharField(
        max_length=32,
        null=False
    )

    patronymic = models.CharField(
        max_length=32,
        null=False
    )

    surname = models.CharField(
        max_length=32,
        null=False
    )

    birth = models.DateField(
        null=False
    )

    email = models.EmailField(
        null=False
    )

    phone = models.CharField(
        max_length=12
    )

    start_work = models.DateField(
        null=False,
    )

    finish_work = models.DateField(
        null=True
    )

    position = models.CharField(
        max_length=32,
        null=False
    )

    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.name} {self.patronymic} {self.surname}'

    @classmethod
    def filter_by_unit_and_working(cls, unit=None, is_working=None):
        '''
        Возвращает сотрудников отфильтрованных по отделу и статусу (работает или нет)
        :param unit: название отдела
        :param is_working: работающие (True) или все
        :return: queryset
        '''
        if not unit and not is_working:
            return cls.objects.all().order_by('surname')
        q = Q()
        if is_working:
            q &= Q(finish_work=None)
        if unit:
            unit_ = Unit.objects.filter(title=unit)
            try:
                unit_id = unit_[0].id
            except IndexError:
                pass
            else:
                q &= Q(unit_id=unit_id)
        return cls.objects.filter(q).order_by('surname')

    @classmethod
    def get_range(cls, start, stop=None):
        '''
        Возвращает сотрудников, у которых фамилии начинаются на буквы в диапазоне [start, stop]
        :param start: начало диапазона
        :param stop: конец диапазона (вкл.)
        :return: queryset
        '''
        try:
            start_index = ALPHAS.index(start)
            stop_index = ALPHAS.index(stop) if stop else start_index
            query = cls.objects.filter(
                reduce(
                    lambda q_obj, surname: q_obj | Q(surname__startswith=surname),
                    ALPHAS[start_index: stop_index + 1], Q()
                )
            ).order_by('surname')
        except ValueError:
            query = cls.objects.all()
        return query

    @classmethod
    def get_groups(cls, groups_num):
        '''
        Возвращает список групп пользователей по фамилиям
        :param groups_num: количество групп
        :return: list
        '''
        one_group_contains = cls.objects.all().count() // groups_num
        d = OrderedDict()
        for char in ALPHAS:
            d[char] = cls.objects.filter(surname__startswith=char).count()
        groups = []
        for key, val in d.items():
            if not groups:
                groups.append({'chars': [key], 'count': val})
            if not val:
                continue
            if groups[-1]['count'] + val <= one_group_contains \
                    or groups[-1]['count'] < one_group_contains / 2 \
                    or groups[-1]['count'] + val < one_group_contains * 1.1:
                groups[-1]['chars'].append(key)
                groups[-1]['count'] += val
            else:
                groups.append({'chars': [key], 'count': val})
        return list(map(lambda x: (x['chars'][0], x['chars'][-1]), groups))
