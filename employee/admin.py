# admin.py
from django.contrib import admin
from .models import Employee
from .models import EmployeeMonthlyData


class EmployeeMonthlyDataAdmin(admin.ModelAdmin):
    list_display = ('employee_first_name', 'employee_last_name', 'employee_id', 'month', 'salary', 'total_km', 'total_transport', 'total_food', 'total_parking')

    def employee_first_name(self, obj):
        return obj.employee.first_name

    def employee_last_name(self, obj):
        return obj.employee.last_name

    def employee_id(self, obj):
        return obj.employee.id

    employee_id.short_description = 'ID'
    employee_first_name.short_description = 'First Name'
    employee_last_name.short_description = 'Last Name'



admin.site.register(EmployeeMonthlyData, EmployeeMonthlyDataAdmin)

admin.site.register(Employee)