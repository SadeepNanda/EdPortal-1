from django.shortcuts import render,redirect


# Create your views here.
def create_course_request(request):
    print(request.session['sid'])
    print('Ok we can add course requests')
    print(request.POST)

    return redirect('show_all_courses')

