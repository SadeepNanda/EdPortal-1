from django.urls import path,include
from . import views

urlpatterns = [

    path('course_request/',views.create_course_request,name='create_course_request'),



]