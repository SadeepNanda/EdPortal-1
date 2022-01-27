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
        print(form.is_valid())
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
        print(form)
        print(form.is_valid())
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
        #print(form)
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
    course = courses.objects.all()
    course1 = [course for course in courses.objects.all()]
    not_displayable_courses = [course.registered_course_id for course in student_teachers.objects.filter(
        student_id=student.objects.get(student_id=request.session['sid']))]
    # print(not_displayable_courses)
    # print(type(course))
    displayable_courses = []
    for crs in course1:
        if crs not in not_displayable_courses:
            displayable_courses.append(crs)

    # print(displayable_courses)
    # displayable_courses=[course1 for course1 in course and not in not_displayable_courses  ]

    requested_courses_list= [course.requested_course_id for course in course_requests.objects.filter(
        requested_student_id=student.objects.get(student_id=request.session['sid'])).filter(approval_status='Pending')]

    print(requested_courses_list)

    final_displayable_course=[]
    for crs in displayable_courses:
        if crs not in requested_courses_list:
            final_displayable_course.append(crs)
    #print(final_displayable_course)
    #print(final_displayable_course[1].course_name)

    if 'msg' not in request.POST:
        return render(request, 'students\show_all_courses.html', {'course': final_displayable_course})
    else:
        #print(final_displayable_course)
        filtered_courses_list=[]
        if request.POST['msg']=='Search':
            for idx in range(len(final_displayable_course)):
                crs=final_displayable_course[idx]
                #print(crs,crs.course_name)
                #print(crs.course_name,request.POST['course_name'])
                #print(crs.course_name==request.POST['course_name'])
                if crs.course_name==request.POST['course_name'] or crs.course_type==request.POST['course_type'] or crs.course_instructor_id.name==request.POST['course_instructor']:
                    #print(final_displayable_course.index(crs))
                    filtered_courses_list.append(crs)
            return render(request, 'students\show_all_courses.html', {'course': filtered_courses_list})

    # applicable_courses=[course for course in courses.objects.filter(course_id=)]
    return render(request, 'students\show_all_courses.html', {'course': final_displayable_course})


def show_student_profile(request):
    if request.session.has_key('sid') or request.session.has_key('tid') :
        try:
            student_info=student.objects.get(student_id=int(request.POST['student_id']))

            #print(request.POST)

        except:
            student_info = student.objects.get(student_id=int(request.session['sid']))

        return render(request,'students\show_student_profile.html',{'student_info':student_info})
    else:
        return  redirect('Landing')


def show_my_courses(request):
    if request.session.has_key('sid')  :
        my_courses=student_teachers.objects.filter(student_id=student.objects.get(student_id=request.session['sid']))
        print(my_courses)

        print(request.POST)

        return render(request,'students\show_my_courses.html',{'my_courses':my_courses})
    else:
        return  redirect('slogin')

def show_requested_courses(request):
    if request.session.has_key('sid'):
        requested_courses_list = [course.requested_course_id for course in course_requests.objects.filter(
            requested_student_id=student.objects.get(student_id=request.session['sid'])).filter(
            approval_status='Pending')]

        requests_list= [course for course in course_requests.objects.filter(
            requested_student_id=student.objects.get(student_id=request.session['sid'])).filter(
            approval_status='Pending')]

        #print(requested_courses_list)
        #print(requested_courses_list.values("requested_course_id").course_name)
        #print("These are the requested courses")
        return  render(request,'students\show_requested_courses.html',{'courses':requested_courses_list,'requests':requests_list})
    else:
        return redirect('slogin')


def show_notifications(request):
    if request.session.has_key('sid'):
        ntfs=notifications.objects.filter(s_id = student.objects.get(student_id=request.session['sid'])).order_by('-created_at')
        #ntfs=notifications.objects.filter(s_id)
        return render(request,'students/notifications.html',{'ntfs':ntfs})
    else:
        return redirect('slogin')












