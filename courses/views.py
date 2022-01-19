
from django.shortcuts import render,redirect


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
    # print(list(request.POST.keys()))

    return redirect('show_all_courses')

