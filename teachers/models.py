from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
from django.core.validators import RegexValidator
from students.models import *

class teachers(models.Model):
    teacher_id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, null=False, blank=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    subject=models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    ratings = models.DecimalField(default=0.0,decimal_places=2,validators=[MaxValueValidator(5.0),MinValueValidator(0.1)],max_digits=3,blank=True)
    username=models.CharField(max_length=100,null=False,blank=False)
    password = models.CharField(max_length=100, null=False, blank=False)

#class course_requests(models.Model):
#    requested_course_id=models.ForeignKey(student,on_delete=models.CASCADE)
#    requested_created_at = models.DateTimeField(auto_now_add=True)
#    approval_status=models.CharField(max_length=50)





