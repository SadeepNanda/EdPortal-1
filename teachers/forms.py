from .models import teachers
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from courses.models import courses


class teacher_creation_form(forms.ModelForm):
    name = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)
    phone_number =  forms.CharField(max_length=17)
    subject = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True,max_length=30)
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}),required=True,max_length=30)
    class Meta:
        model = teachers
        fields = (
            'name',
            'email',
            'phone_number',
            'subject',
            'address',
            'username',
            'password',
        )

class teacher_login_form(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
                               required=True, max_length=30)
    class Meta:
        fields = (
            'username',
            'password',
        )

class course_creation_form(forms.ModelForm):
    course_name = forms.CharField(max_length=100)
    course_type = forms.CharField(max_length=100)
    course_description = forms.CharField(max_length=500)

    class Meta:
        model = courses
        fields = (
            'course_name',
            'course_type',
            'course_description',
        )


