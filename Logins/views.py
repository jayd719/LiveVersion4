from django.shortcuts import render,redirect
from .forms import CBBLiveUserReg
from django.contrib import messages
from django.contrib.auth import authenticate, login
from homepage.functions import userInfo


ERROR="Please note that as we're in the development stage, accounts are valid for 15 days. If your account expires, feel free to create another one. We appreciate your understanding and look forward to your continued involvement in our project!"

def signUpPage(requests):
    context = {'form':CBBLiveUserReg(),'title':'Create Account'}   
    if requests.method=="POST":
            form = CBBLiveUserReg(requests.POST)
            if form.is_valid():
                user = form.save()
                user.is_staff = False
                user.save()
                username=form.cleaned_data.get('username')
                messages.success(requests,f'Account Created For {username}!')
                userInfo(requests)
                return redirect('home-main')
                
    else:
        messages.error(requests,'Error Please Try Again')
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