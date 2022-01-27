from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime

from sqlalchemy import null


class student(models.Model):
	student_id=models.AutoField(primary_key=True)
	#code = models.CharField(max_length=10,unique=True)
	name= models.CharField(max_length=50)
	email = models.EmailField(max_length=50,null=False,blank=False)
	contact_no = models.IntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])
	dept= models.CharField(max_length=50,null=False,blank=False)
	#image=models.ImageField(upload_to='image/%Y/%m/%d/',max_length=50,null=True,blank=True)
	address= models.CharField(max_length=100,null=False,blank=False)
	username=models.CharField(max_length=100,null=False,blank=False)
	password=models.CharField(max_length=100,null=False,blank=False)
	Class = models.CharField(max_length=20, null=True)
	board = models.CharField(max_length=100, null=False, default="Central Board of Secondary Education")

class notifications(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	msg= models.CharField(max_length=500)
	s_id=models.ForeignKey(student,on_delete=models.CASCADE)



#class Courses(models.Model):

