from shutil import _ntuple_diskusage
from django.db import models
from statistics import mode

# Create your models here.
class Employee(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    id = models.CharField(max_length=9, primary_key = True)
    email = models.CharField(max_length=30)
    cell_phone = models.CharField(max_length=30, null=True)
    construction_hours = models.FloatField(null=True, default=0,max_length=30)
    dismantling_hours = models.FloatField(null=True, default=0,max_length=30)
    total_km = models.FloatField(null=True, default=0)
    total_transport = models.FloatField(null=True, default=0)
    total_food = models.FloatField(null=True, default=0)
    total_parking = models.FloatField(null=True, default=0)
    hourly_wage = models.FloatField(null=True, default=35)
    salary = models.FloatField(null=True, default=0)
    shift_start_date_time = models.DateTimeField(null=True)
    shift_end_date_time = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"  # Returns full name

class EmployeeMonthlyData(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.DateField()
    salary = models.FloatField()
    total_km = models.FloatField()
    total_transport = models.FloatField()
    total_food = models.FloatField()
    total_parking = models.FloatField()

    def __str__(self):
        return f'{self.employee.first_name} {self.employee.last_name} - {self.month.strftime("%B %Y")}'
