from django.contrib import admin

from . models import *
admin.site.register(courses)
admin.site.register(course_requests)
admin.site.register(student_teachers)
# Register your models here.
