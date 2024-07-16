from django.db import models

# Create your models here.
class EmployeesWaitingForApproval(models.Model):
    user_name = models.CharField(max_length=30, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    id = models.CharField(max_length=9, primary_key = True)
    email = models.CharField(max_length=30)
    cell_phone = models.CharField(max_length=30, null=True)
    pass1 = models.CharField(max_length=30,null=True)
    pass2 = models.CharField(max_length=30,null=True)