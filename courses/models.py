
from django.db import models
from teachers.models import teachers
from students.models import student
from django.core.validators import MaxValueValidator, MinValueValidator

class courses(models.Model):
    course_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    course_name= models.CharField(max_length=50,null=False)
    course_type= models.CharField(max_length=50,null=False)
    course_description= models.TextField(max_length=500,null=False)
    course_instructor_id=models.ForeignKey(teachers,on_delete=models.CASCADE)
    course_class_strength=models.IntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(300)])
    course_meet_link = models.CharField(max_length=150, null=True)

class course_requests(models.Model):
    requested_course_id=models.ForeignKey('courses',on_delete=models.CASCADE)
    course_instructor_id=models.ForeignKey(teachers,on_delete=models.CASCADE)
    requested_student_id=models.ForeignKey(student,on_delete=models.CASCADE)
    approval_status=models.CharField(max_length=50)

class student_teachers(models.Model):
    registered_course_id = models.ForeignKey(courses, on_delete=models.CASCADE)
    course_instructor_id = models.ForeignKey(teachers, on_delete=models.CASCADE)
    student_id = models.ForeignKey(student, on_delete=models.CASCADE)

class notes(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=500)
    s_id = models.ForeignKey(student, on_delete=models.CASCADE)
    course_id=models.ForeignKey(courses, on_delete=models.CASCADE)

class resources(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    course_id = models.ForeignKey(courses, on_delete=models.CASCADE)
    resource = models.FileField(null=True)
    description=models.CharField(max_length=200,null=True)