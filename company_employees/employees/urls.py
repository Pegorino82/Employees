from django.urls import path

from employees.views import EmployeesListView, EmployeesSurnameView, EmployeeDetailView, index

app_name = 'employees'

urlpatterns = [
    path('', index, name='index'),
    path('employees', EmployeesListView.as_view(), name='list'),
    path('employees/surname', EmployeesSurnameView.as_view(), name='list_by_surname'),
    path('employees/<int:pk>', EmployeeDetailView.as_view(), name='detail'),
]
