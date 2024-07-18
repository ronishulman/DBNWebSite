# admin.py
from django.contrib import admin
from .models import EmployeesWaitingForApproval

admin.site.register(EmployeesWaitingForApproval)