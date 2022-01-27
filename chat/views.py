from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import *
from teachers.models import *
from students.models import *


# Create your views here.
def messages_page(request):
    first_person = None
    if request.method=='POST' and request.POST :
        print(request.POST)
        #if request.session.has_key('sid'):
        #print(request.POST['logged-in-user'])


        if request.POST['logged_in_as']:
            if request.POST['logged_in_as']=='student':
                first_person=ChatUsers.objects.get(student_profile=student.objects.get(student_id=request.POST['student_id']))
            else:
                first_person = ChatUsers.objects.get(teacher_profile=request.POST['teacher_id'].teacher_id)

        #    print(first_person)
        #second_person=ChatUsers.objects.get(teacher_profile=request.POST['teacher_id'])
        threads = Thread.objects.by_user(user=first_person).prefetch_related('chatmessage_thread').order_by('timestamp')
        # threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
        # threads=[]
        print(threads)
        context = {
            'Threads': threads,
            'first_person': first_person,
            'logged_in': first_person,

        }
        return render(request, "chat/messages.html", context)


    else:
        threads = Thread.objects.by_user(user=first_person).prefetch_related('chatmessage_thread').order_by('timestamp')
        # threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
        # threads=[]
        print(threads)
        context = {
            'Threads': threads,
            'first_person': first_person,
            'logged_in': first_person,

        }
        return render(request, "chat/messages.html", context)



