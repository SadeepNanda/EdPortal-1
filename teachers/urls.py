from django.urls import path,include
from . import views

urlpatterns = [


    path('teacher_registration/',views.teacher_registration, name='tregistration'),
    path('teacher_login/',views.teacher_login, name='tlogin'),
    path('teacher_home/',views.teacher_home, name='thome'),
    path('teacher_logout/',views.teacher_logout,name='tlogout'),
    path('course_creation/',views.create_course,name='coursecreate'),
    path('display_my_course/',views.display_my_courses,name='teachercourses')




]