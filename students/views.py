from django.shortcuts import render,redirect
from . forms import *
from .models import *
from django.views.decorators.cache import cache_control
from courses.models import *

def landing(request):
    return render(request,'students/landing_page.html',{})
def student_registration(request):
    if request.method=='POST':
        print(request.POST)
        form=student_creation_form(request.POST)
        if form.is_valid():
            student=form.save(commit="False")
            student.save()

        return redirect('slogin')
    else:
        form=student_creation_form()
        return render(request,'students/student_registration.html',{'form':form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def student_login(request):
    if request.method=='POST':
        print(request.POST)
        form=student_login_form(request.POST)
        if form.is_valid():
            username=request.POST['username']
            s=student.objects.get(username=username)
            password=s.password
            sid=s.student_id
            print(password)
            if password==request.POST['password']:
                request.session['sid']=sid
                request.session['logged in']=True
                return redirect('shome')
            else:
                msg="Wrong password or username"
                return  render(request,'students/student_login.html',{'msg':msg,'form':form})




    else:
        form=student_login_form()
        return  render(request,'students/student_login.html',{'form':form})

def student_logout(request):
    del request.session['sid']
    return redirect('slogin')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def student_home(request):
    if request.session.has_key('sid'):
        s=student.objects.get(student_id=request.session['sid'])
        msg='Welcome '+s.name
        return render(request,'students/student_home.html',{'msg':msg})
    else:
        return redirect('slogin')

def show_all_courses(request):
    course=courses.objects.all()
    return  render(request,'students\show_all_courses.html',{'course':course})









