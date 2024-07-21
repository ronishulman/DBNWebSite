# admin.py
from django.contrib import admin
from .models import Employee
from .models import EmployeeMonthlyData

admin.site.register(Employee)
admin.site.register(EmployeeMonthlyData)