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
