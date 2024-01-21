from django.shortcuts import render,redirect
from .forms import CBBLiveUserReg
from django.contrib import messages
from django.contrib.auth import authenticate, login

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
        form = CBBLiveUserReg()
    return render(requests,'login/registar.html',{'form':form,'title':'Create Account'})


# def signIn(requests):
#     if requests.method=="POST":
#         username = requests.POST["Username"]
#         password = requests.POST["password"]
#         user = authenticate(requests, username=username, password=password)
#         if user is not None:
#             login(requests, user)
#             return redirect('home-main')
            
#     return render(requests,'login/signIn.html')