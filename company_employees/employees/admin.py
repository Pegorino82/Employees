from django.contrib import admin

from employees.models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'patronymic',
        'surname',
        'birth',
        'email',
        'phone',
        'start_work',
        'finish_work',
        'position',
        'unit_name'
    ]

    search_fields = [
        'surname',
        'position',
        'unit__title',
    ]

    def unit_name(self, obj):
        return obj.unit.title


admin.site.register(Employee, EmployeeAdmin)
