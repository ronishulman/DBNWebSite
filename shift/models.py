from statistics import mode
from django.db import models

# Create your models here.
class Shift(models.Model):
    first_name= models.CharField(max_length=30)
    last_name= models.CharField(max_length=30)
    employee_id = models.IntegerField(max_length=9)
    shift_id = models.AutoField(primary_key=True)
    shift_start_date_time = models.DateTimeField(null=True)
    shift_end_date_time = models.DateTimeField(null=True)
    type_of_shift = models.CharField(max_length=100, null= True)
    length_of_the_shift = models.FloatField(null=True)
    client= models.CharField(max_length=30, null=True)
    location= models.CharField(max_length=30, null=True)
    amount_of_km= models.FloatField(max_length=30, null= True, blank=True, default=0)
    public_transport= models.FloatField(max_length=30, null= True,blank=True, default=0)
    food= models.FloatField(max_length=30, null=True,blank=True, default=0)
    shift_pay = models.FloatField(max_length=30, null=True, default=0)
    parking_refund = models.FloatField(max_length=30, null= True, blank=True, default=0)
    parking_receipt = models.ImageField(null=True, blank=True, upload_to="images/")

class TempShift(models.Model):
    pass


    
    