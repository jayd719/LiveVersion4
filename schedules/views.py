from django.shortcuts import render,HttpResponse

def shd_home(requests):
    return render(requests,'homepage.html')

# Create your views here.
