from django.shortcuts import render
from django.views.generic import ListView, DetailView
from employees.models import Employee
from units.models import Unit

from django.db.models import Q


def index(request):
    return render(request, template_name='employees/index.html', context={'title': 'Main'})


class EmployeesListView(ListView):
    model = Employee
    queryset = Employee.objects.all().order_by('surname')
    template_name = 'employees/employees.html'
    extra_context = {
        'title': 'employees list',
        'units': Unit.objects.all()
    }

    def get(self, request, *args, **kwargs):
        unit = request.GET.get('unit')
        is_working = request.GET.get('is_working')
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
        self.queryset = Employee.objects.filter(q).order_by('surname')
        self.paginate_by = 7
        return super(EmployeesListView, self).get(request, *args, **kwargs)


class EmployeesSurnameView(ListView):
    model = Employee
    template_name = 'employees/employees_by_surname.html'
    extra_context = {
        'title': 'employees by surname',
        'borders': Employee.get_groups(6)
    }

    def get(self, request, *args, **kwargs):
        start = request.GET.get('start')
        stop = request.GET.get('stop')
        if start and stop:
            self.queryset = Employee.get_range(start, stop)
        else:
            self.queryset = Employee.get_range('А', 'Г')
        self.paginate_by = 7
        return super(EmployeesSurnameView, self).get(request, *args, **kwargs)


class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'employees/detail.html'
    context_object_name = 'employee'

    extra_context = {
        'title': 'employee detail',
    }
