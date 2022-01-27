from django.shortcuts import render,redirect
from .forms import *
from.models import *
from django.views.decorators.cache import cache_control
from courses.models import *
from students.models import *
from django.http import HttpResponse

#teachers
def teacher_registration(request):
    if request.method=='POST':
        print(request.POST)
        form = teacher_creation_form(request.POST, request.FILES)
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
            print(form.is_valid())
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


def display_my_courses(request):
    if request.session.has_key('tid'):
        teacher_course_list=[course for course in courses.objects.filter(course_instructor_id=teachers.objects.get(teacher_id=request.session['tid']))]
        print(teacher_course_list)


        return  render(request,'teachers/teacher_my_courses.html',{'mycourses':teacher_course_list})
    else:
        return redirect('tlogin')


def display_my_requests(request):
    if request.session.has_key('tid'):



        #course_approval
        if 'msg' in request.POST.keys() and request.POST['msg']=='Approve':
            course_request=course_requests.objects.get(id=request.POST['request_id'])
            course_request.approval_status='Approved'
            course_request.save()
            course_request.requested_course_id.course_class_strength+=1
            course_request.requested_course_id.save()
            s_teacher_register=student_teachers(registered_course_id=course_request.requested_course_id,course_instructor_id=course_request.course_instructor_id,student_id=course_request.requested_student_id)
            s_teacher_register.save()
            notification = notifications()
            notification.msg = 'Accepted Request!\nYour requested for enrollment in course ' + course_request.requested_course_id.course_name + ' by: ' + course_request.course_instructor_id.name + 'has been accepted by the course instructor'
            notification.s_id = student.objects.get(student_id=course_request.requested_student_id.student_id)
            notification.save()

        teacher_course_request_list = [course_request for course_request in course_requests.objects.filter(
            course_instructor_id=teachers.objects.get(teacher_id=request.session['tid'])).filter(
            approval_status='Pending')]
        print(teacher_course_request_list)


        return  render(request,'teachers/course_requests.html',{'course_requests':teacher_course_request_list})
    else:
        return redirect('tlogin')

def show_teacher_profile(request):
    if request.session.has_key('sid') or request.session.has_key('tid') :
        try:
            teacher_info=teachers.objects.get(teacher_id=int(request.POST['teacher_id']))

            print(request.POST)
        except:
            teacher_info = teachers.objects.get(teacher_id=int(request.session['tid']))


        return render(request,'teachers\show_teacher_profile.html',{'teacher_info':teacher_info})
    else:
        return  redirect('Landing')





