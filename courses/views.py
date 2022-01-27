from django.shortcuts import render,redirect
from .models import *
from students.models import *


# Create your views here.
def create_course_request(request):
    print(request.session['sid'])
    print('Ok we can add course requests')
    print(request.POST)

    course_request = course_requests()
    course = courses.objects.get(course_id=request.POST['course_id'])
    course_request.requested_course_id = course
    course_request.course_instructor_id = course.course_instructor_id
    course_request.requested_student_id = student.objects.get(student_id=request.session['sid'])
    course_request.approval_status = 'Pending'
    course_request.save()
    notification=notifications()
    notification.msg='You have requested for enrollment in course '+course.course_name+' by: '+course.course_instructor_id.name
    notification.s_id=student.objects.get(student_id=request.session['sid'])
    notification.save()
    # print(list(request.POST.keys()))




    return redirect('show_all_courses')

def show_course_details(request):
    if request.session.has_key('sid'):
        print(request.POST)
        course_details=None
        student_details=student.objects.get(student_id=request.session['sid'])
        try:
            course_details=courses.objects.get(course_id=request.POST['course_id'])
            nts=notes.objects.filter(course_id=course_details).filter(s_id=student_details).order_by('-created_at')

        except:
            print(request.POST['course'])
            #note=notes(note=request.POST['note'],s_id=student_details,course_id=request.POST['course'])
            #note.save()
            course_details=courses.objects.get(course_id=request.POST['course'])
            note = notes(note=request.POST['note'], s_id=student_details, course_id=course_details)
            note.save()
            nts = notes.objects.filter(course_id=course_details).filter(s_id=student_details).order_by('-created_at')
            print(note)




        return render(request,'courses/view_course_details.html',{'crs':course_details,'nts':nts})
    else:
        redirect('slogin')
    #return render(request, 'courses/courses.html', {'crs': course_details})


def modify_course_details(request):
    if request.session.has_key('tid'):
        try:
            print(request.POST)
            course_details = courses.objects.get(course_id=request.POST['course_id'])
            resource=resources.objects.filter(course_id=course_details)
            print(resource)

            return render(request, 'courses/courses.html', {'crs':course_details})
        except:
            print(request.POST)
            print(request.FILES)

            course_details = courses.objects.get(course_id=request.POST['course'])
            resource = resources(course_id=course_details,resource=request.FILES['resource_file'],description='new notes')
            resource.save()

            return render(request, 'courses/courses.html', {'crs':course_details})
    else:
        redirect('tlogin')
    # return render(request, 'courses/courses.html', {'crs': course_details})




def delete_request(request):
    print(request.POST)
    print("Delete request")
    print(course_requests.objects.get(id=request.POST['request_id']))
    course_request = course_requests.objects.get(id=request.POST['request_id'])
    course_requests.objects.get(id=request.POST['request_id']).delete()

    if request.POST['access_type']=='student':
        notification = notifications()
        notification.msg = 'You have deleted your requested for enrollment in course ' + course_request.requested_course_id.course_name + ' by: ' + course_request.course_instructor_id.name
        notification.s_id = student.objects.get(student_id=request.session['sid'])
        notification.save()
        return  redirect('/show_requested_courses/')
    else:
        notification = notifications()
        notification.msg = 'Rejected Request!\nYour requested for enrollment in course ' + course_request.requested_course_id.course_name + ' by: ' + course_request.course_instructor_id.name +'has been rejected by the course instructor'
        notification.s_id = student.objects.get(student_id=request.session['sid'])
        notification.save()
        return redirect('teacherrequests')