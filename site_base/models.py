from django.db import models
from django.contrib.auth.models import User

#Create your models here.
class WorkSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    day = models.CharField(max_length=30)
    client = models.CharField(max_length=30)
    type_of_shift = models.CharField(max_length=100, null= True)
    beginning_time = models.CharField(max_length=30)
    num_of_employees = models.CharField(max_length=30)
    name_of_employees = models.TextField(null=True)
    location = models.CharField(max_length=30, null=True)
    notes = models.TextField(null=True, blank=True)

