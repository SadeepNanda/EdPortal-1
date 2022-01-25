from django.urls import path,include
from . import views

urlpatterns = [

    path('course_request/',views.create_course_request,name='create_course_request'),
    path('course_details/',views.show_course_details,name='course_details'),
    path('delete_request/',views.delete_request,name='delete_request'),




]