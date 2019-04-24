from django.shortcuts import render
from django.views.generic import ListView, DetailView
from employees.models import Employee
from units.models import Unit


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
        self.queryset = Employee.filter_by_unit_and_working(unit, is_working)
        self.paginate_by = 7
        return super(EmployeesListView, self).get(request, *args, **kwargs)


class EmployeesSurnameView(ListView):
    model = Employee
    template_name = 'employees/employees_by_surname.html'
    borders = None

    def get(self, request, *args, **kwargs):
        self.borders = Employee.get_groups()
        start = request.GET.get('start')
        stop = request.GET.get('stop')
        self.queryset = Employee.get_range(start, stop)
        self.paginate_by = 7
        return super(EmployeesSurnameView, self).get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'employees by name'})
        context.update({'borders': self.borders})
        return context


class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'employees/detail.html'
    context_object_name = 'employee'
    extra_context = {
        'title': 'employee detail',
    }
