from django.contrib import admin

from units.models import Unit


class UnitAdmin(admin.ModelAdmin):
    list_display = [
        'title',
    ]


admin.site.register(Unit, UnitAdmin)
