from django.shortcuts import render,redirect
from .forms import *
from.models import *
from django.views.decorators.cache import cache_control
from courses.models import courses
#teachers
def teacher_registration(request):
    if request.method=='POST':
        print(request.POST)
        form = teacher_creation_form(request.POST)
        if form.is_valid():
            teacher = form.save(commit="False")
            teacher.save()
        return redirect('tlogin')

    else:
        form=teacher_creation_form()
        return render(request,'teachers/teacher_registration.html',{'form':form})


def teacher_login(request):
    if request.method == 'POST':
        print(request.POST)
        form = teacher_login_form(request.POST)
        if form.is_valid():
            username = request.POST['username']
            t = teachers.objects.get(username=username)
            password = t.password
            tid = t.teacher_id
            print(password)
            if password == request.POST['password']:
                request.session['tid'] = tid
                request.session['logged_in'] = True
                return redirect('thome')
            else:
                msg = "Wrong password or username"
                return render(request, 'teachers/teacher_login.html', {'msg': msg, 'form': form})
    else:
        form=teacher_login_form()
        return  render(request,'teachers/teacher_login.html',{'form':form})


def teacher_logout(request):
    print(request.session['tid'])
    del request.session['tid']
    return redirect('tlogin')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def teacher_home(request):
    if request.session.has_key('tid'):
        t=teachers.objects.get(teacher_id=request.session['tid'])
        msg='Welcome '+t.name
        return render(request,'teachers/teacher_home.html',{'msg':msg})
    else:
        return redirect('tlogin')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def create_course(request):
    if request.session.has_key('tid'):
        if request.method=='POST':
            print(request.POST)
            form = course_creation_form(request.POST)
            if form.is_valid():
                print(form)
                #print(course)
                course=courses(course_name=request.POST['course_name'],
                               course_type=request.POST['course_type'],
                               course_description=request.POST['course_description'],
                               course_instructor_id=teachers.objects.get(teacher_id=request.session['tid']),
                               course_class_strength=0
                               )
                course.save()
            return render(request, 'teachers/course_creation.html', {'form': form})
        else:
            form=course_creation_form()
            return render(request,'teachers/course_creation.html',{'form':form})
    else:
        return redirect('tlogin')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def display_my_courses(request):
    if request.session.has_key('tid'):
        teacher_course_list=[course for course in courses.objects.filter(course_instructor_id=teachers.objects.get(teacher_id=request.session['tid']))]
        print(teacher_course_list)
        print(type(teacher_course_list[1]))

        return  render(request,'teachers/teacher_my_courses.html',{'mycourses':teacher_course_list})
    else:
        return redirect('tlogin')

