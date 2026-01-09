from django.db import models
from django.utils import timezone

# Create your models here.
class admin_table(models.Model):
    user_name = models.CharField(max_length=30)
    password= models.CharField(max_length=150) 

class katha_table(models.Model):
    user_name = models.CharField(max_length=30)
    password= models.CharField(max_length=250) 
    phone_number = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    
class payment_table(models.Model):
    user_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=50)
    address = models.CharField(max_length=100,default="manchiryal")
    type = models.CharField(max_length=100,default="normal")  
    mode = models.CharField(max_length=100,default="cash")  
    amount = models.CharField(max_length=20) 
    total = models.IntegerField(default=1) 
    purchase_date = models.DateField(default=timezone.now)

