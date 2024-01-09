from django.shortcuts import render,redirect
from .forms import CBBLiveUserReg
from django.contrib import messages

def signUpPage(requests):
    context = {'form':CBBLiveUserReg(),'title':'Create Account'}
    if requests.method=="POST":
            form = CBBLiveUserReg(requests.POST)
            if form.is_valid():
                form.save()
                username=form.cleaned_data.get('username')
                messages.success(requests,f'Account Created For {username}!')
                return redirect('home-main')  
            else:
                messages.info(requests,'Try Again')
               
    return render(requests,'login/registar.html',context)

