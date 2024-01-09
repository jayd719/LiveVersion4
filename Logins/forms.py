from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

COMPANIES = (
        (1,'Live'),
        (2,'CBB')
    )



class CBBLiveUserReg(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField()
    class Meta:
        model = User
        fields =['first_name','last_name','username','email','password1','password2']