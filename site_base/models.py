from django.db import models
from django.contrib.auth.models import User
from employee.models import Employee

#Create your models here.
class WorkSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    day = models.CharField(max_length=30)
    client = models.CharField(max_length=30)
    type_of_shift = models.CharField(max_length=100, null= True)
    beginning_time = models.CharField(max_length=30)
    num_of_employees = models.PositiveIntegerField() 
    employees = models.ManyToManyField(Employee, related_name='shifts', blank=True)
    location = models.CharField(max_length=30, null=True)
    notes = models.TextField(null=True, blank=True)

class UpdateMessages(models.Model):
    message = models.TextField()
    employee = models.ForeignKey(Employee , on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name}: {self.message}"

