from django.shortcuts import render,redirect
from .forms import CBBLiveUserReg
from django.contrib import messages
from django.contrib.auth import authenticate, login

def signUpPage(requests):
    context = {'form':CBBLiveUserReg(),'title':'Create Account'}
    if requests.method=="POST":
            form = CBBLiveUserReg(requests.POST)
            if form.is_valid():
                try:
                    form.save()
                except:
                    messages.info(requests,'User With Similar Username Or Email ID Already Exists, Try Again With Different Credentials')
                username=form.cleaned_data.get('username')
                messages.success(requests,f'Account Created For {username}!')
                return redirect('home-main')
            else:
                messages.info(requests,'Provided Information Did Meet The Required Enctyption Standard, Try Again')
               
    return render(requests,'login/registar.html',context)


# def signIn(requests):
#     if requests.method=="POST":
#         username = requests.POST["Username"]
#         password = requests.POST["password"]
#         user = authenticate(requests, username=username, password=password)
#         if user is not None:
#             login(requests, user)
#             return redirect('home-main')
            
#     return render(requests,'login/signIn.html')