
from django.urls import path,include
from . import views
from courses import views as courses_views

urlpatterns = [

    path('',views.landing, name='Landing' ),
    path('student_registration/',views.student_registration, name='sregistration'),
    path('student_login/',views.student_login, name='slogin'),
    path('student_home/',views.student_home, name='shome'),
    path('student_logout/',views.student_logout, name='slogout'),
    path('show_courses/',views.show_all_courses, name='show_all_courses'),
    path('course_request/',courses_views.create_course_request,name='create_course_request'),





]