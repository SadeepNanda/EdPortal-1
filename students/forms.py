from django import forms
from .models import student
from django.core.validators import MaxValueValidator, MinValueValidator

class student_creation_form(forms.ModelForm):
    name = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)
    contact_no = forms.IntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])
    dept = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True,max_length=30)
    address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True,max_length=30)
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}),required=True,max_length=30)
    class Meta:
        model = student
        fields = (
            'name',
            'email',
            'contact_no',
            'dept',
            'address',
            'username',
            'password',
        )

class student_login_form(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
                               required=True, max_length=30)
    class Meta:
        fields = (
            'username',
            'password',
        )